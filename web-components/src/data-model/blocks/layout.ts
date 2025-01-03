import { markRaw } from 'vue'

import VCompute from '@/components/controls/ComputeConnector.vue'
import VGroup from '@/components/layout/Group.vue'
import VSelect from '@/components/layout/SelectBlock.vue'
import VToggle from '@/components/layout/Toggle.vue'

import { useLayoutStore, useViewStore } from '../layout-store'
import { type EmptyObject } from '../root-store'
import { SwapType } from '../types'
import * as b from './index'
import { ControlsField } from './interactive'
import { Block, type BlockFigure } from './leaf-blocks'

export abstract class ParentBlock<T extends Block = Block> extends Block {
  /**
   * A non-atomic block that has children
   */
  public children: T[]

  public constructor(elem: any, figure: BlockFigure) {
    super(elem, figure)
    const { blocks } = elem as unknown as { blocks: any[] }
    this.children = blocks
  }
}

export abstract class LayoutBlock<
  T extends Block = Block,
> extends ParentBlock<T> {
  /**
   * A non-atomic block which uses children to control layout, e.g. in columns, selects, pages
   */
  public store: any

  public constructor(elem: any, figure: BlockFigure) {
    super(elem, figure)
    this.store = useLayoutStore(this.children)()
    this.componentProps = { ...this.componentProps, store: this.store }
  }

  public update(target: string, group: b.Group, method: SwapType): boolean {
    /**
     * Update the block's children with the given group fragment at the
     * given target ID, if a matching child with ID is found.
     *
     * Returns `true` if the target child was found and updated.
     */
    if (
      this.id === target &&
      (method === SwapType.APPEND || method === SwapType.PREPEND)
    ) {
      this.insertAtEdge(group, method)
      return true
    }

    if (method === SwapType.REPLACE || method === SwapType.INNER) {
      return this.swap(group, target, method)
    }

    return false
  }

  private swap(
    group: b.Group,
    target: string,
    method: SwapType.INNER | SwapType.REPLACE,
  ): boolean {
    /**
     * Replace the child of the given layout block (distinguished by `target`)
     * with the children of the given `View` fragment.
     *
     * Returns `true` if the target child was found and updated.
     *
     * Note: multiple fragment children can replace the single targeted block
     */
    for (const [idx, child] of this.children.entries()) {
      if (child.id === target) {
        if (method === SwapType.REPLACE) {
          this.store.replace(idx, group)
        } else if (method === SwapType.INNER) {
          this.store.inner(idx, group)
        } else {
          throw new Error(`Method ${method} not recognized`)
        }
        return true
      }
    }
    return false
  }

  private insertAtEdge(group: b.Group, method: SwapType) {
    /**
     * Insert the children of a `View` fragment at the beginning or and of a layout block's children
     */
    if (method === SwapType.APPEND) {
      this.store.append(group)
    } else if (method === SwapType.PREPEND) {
      this.store.prepend(group)
    }
  }
}

export class Group extends LayoutBlock {
  public component = markRaw(VGroup)
  public name = 'Group'

  public constructor(elem: any, figure: BlockFigure) {
    super(elem, figure)
    const { columns, widths, valign } = elem as unknown as {
      columns: number
      valign: 'top' | 'center' | 'bottom'
      widths?: string | null
    }
    this.componentProps = {
      ...this.componentProps,
      widths: widths || undefined,
      columns: +columns,
      valign,
    }
  }
}

export class Select extends LayoutBlock {
  public component = markRaw(VSelect)
  public type: string
  public name = 'Select'

  public constructor(elem: any, figure: BlockFigure) {
    super(elem, figure)
    const { label, type } = elem as unknown as {
      label: string
      type: 'dropdown' | 'tabs'
    }
    this.label = label || undefined
    this.type = type
    this.componentProps = { ...this.componentProps, type }
  }
}

export class Toggle extends LayoutBlock {
  public component = markRaw(VToggle)
  public name = 'Toggle'

  public constructor(elem: any, figure: BlockFigure) {
    super(elem, figure)
    const { blocks, label } = elem as unknown as {
      blocks: any[]
      label?: string | null
    }
    this.children = blocks
    this.label = label || undefined
    this.componentProps = { ...this.componentProps, label }
  }
}

export class ComputeBlock extends ParentBlock<ControlsField> {
  public component = markRaw(VCompute)
  public name = 'Compute'

  public constructor(elem: any, figure: BlockFigure) {
    super(elem, figure)
    const { prompt, label, subtitle, action, method } = elem as unknown as {
      label?: string | null
      name?: string | null
      prompt?: string | null
      subtitle?: string | null
      action?: string | null
      method: string
    }
    this.componentProps = {
      ...this.componentProps,
      children: this.children,
      prompt: prompt || 'Submit',
      label,
      subtitle,
      action,
      method,
    }
  }
}

export class View extends LayoutBlock {
  public id = 'root'
  public name = 'View'

  public constructor(elem: any, figure: BlockFigure) {
    super(elem, figure)
    const { fragment } = elem as unknown as { fragment: boolean }

    // FIXME: don't use layout?
    this.store = fragment ? undefined : useViewStore(this.children, undefined)()

    this.componentProps = { ...this.componentProps, store: this.store }
  }
}

/* Block/element type guards and checks */

export const isComputeElem = (elem: Block | b.Elem): boolean =>
  elem._id === 'Compute'

export const isGroupElem = (elem: Block | b.Elem): boolean =>
  elem._id === 'Group'

export const isSelectElem = (elem: Block | b.Elem): boolean =>
  elem._id === 'Select'

export const isToggleElem = (elem: Block | b.Elem): boolean =>
  elem._id === 'Toggle'

export const isViewElem = (elem: Block | b.Elem | EmptyObject): boolean =>
  elem._id === 'View'

export const isParentElem = (elem: Block | b.Elem): boolean =>
  isSelectElem(elem) ||
  isToggleElem(elem) ||
  isViewElem(elem) ||
  isGroupElem(elem) ||
  isComputeElem(elem)

export const isLayoutBlock = (block: Block): block is LayoutBlock =>
  block instanceof LayoutBlock

export const isView = (block: Block | EmptyObject): block is View =>
  block instanceof View
