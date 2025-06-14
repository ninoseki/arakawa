import axios from 'axios'
import { saveAs } from 'file-saver'
import { v4 as uuid4 } from 'uuid'
import { markRaw } from 'vue'

import VAttachmentBlock from '@/components/blocks/Attachment.vue'
import VBigNumberBlock from '@/components/blocks/BigNumber.vue'
import VBigNumberBlockSimple from '@/components/blocks/BigNumberSimple.vue'
import VBokehBlock from '@/components/blocks/BokehConnector.vue'
import VCodeBlock from '@/components/blocks/CodeConnector.vue'
import VEmbedBlock from '@/components/blocks/Embed.vue'
import VFoliumBlock from '@/components/blocks/FoliumConnector.vue'
import VFormulaBlock from '@/components/blocks/FormulaConnector.vue'
import VHTMLBlock from '@/components/blocks/HTML.vue'
import VMediaBlock from '@/components/blocks/Media.vue'
import VPlotlyBlock from '@/components/blocks/PlotlyConnector.vue'
import VSigmaBlock from '@/components/blocks/Sigma/SigmaConnector.vue'
import VSVGBlock from '@/components/blocks/SVGConnector.vue'
import VTableBlock from '@/components/blocks/TableConnector.vue'
import VTextBlock from '@/components/blocks/Text.vue'
import VVegaBlock from '@/components/blocks/VegaConnector.vue'

import { useRootStore } from '../root-store'

// Represents a serialized JSON element prior to becoming a Page/Group/Select/Block
export type Elem = {
  id?: string
  name?: string // for control blocks
  label?: string
  blocks?: Elem[]
  [x: string]: any
}

type AssetResource = Promise<string | object>

export type BlockFigureProps = {
  caption?: string
  captionType: string
  count?: number
}

export type BlockFigure = Pick<BlockFigureProps, 'count' | 'caption'>

export type CaptionType = 'Table' | 'Figure' | 'Plot'

/* Helper functions */

const readGcsTextOrJsonFile = <T = string | object | null>(
  url: string,
): Promise<T> => {
  /**
   * wrapper around `axios.get` to fetch data object of response only
   */
  return axios.get(url).then(res => res.data)
}

/* Inline blocks */

export class Block {
  public refId = uuid4()
  public componentProps: any
  public component: any

  public static captionType: CaptionType = 'Figure'

  public caption?: string
  public label?: string
  public count?: number
  public id?: string
  public name?: string

  public constructor(
    elem: Elem,
    figure: BlockFigure,
    /* eslint-disable-next-line @typescript-eslint/no-unused-vars */
    opts?: unknown,
  ) {
    const { label, id, name } = elem
    this.count = figure.count
    this.caption = figure.caption

    // FIXME: for Storybook's pinia issue...
    const getSingleBlockEmbed = (): boolean | undefined => {
      try {
        const rootStore = useRootStore()
        return rootStore.singleBlockEmbed
      } catch (err) {
        // eslint-disable-next-line no-console
        console.error(err)
      }
      return undefined
    }
    const singleBlockEmbed = getSingleBlockEmbed()

    this.componentProps = { figure, singleBlockEmbed }

    this.id = id
    this.name = name
    this.label = label
  }
}

export class TextBlock extends Block {
  public component = markRaw(VTextBlock)

  public constructor(elem: Elem, figure: BlockFigure, opts?: any) {
    super(elem, figure)
    const { content } = elem as unknown as { content: string }
    this.componentProps = {
      ...this.componentProps,
      content,
      isLightProse: opts.isLightProse,
    }
  }
}

export class CodeBlock extends Block {
  public component = markRaw(VCodeBlock)

  public constructor(elem: Elem, figure: BlockFigure) {
    super(elem, figure)
    const { content, language } = elem as unknown as {
      content: string
      language: string
    }
    this.componentProps = { ...this.componentProps, code: content, language }
  }
}

export class HTMLBlock extends Block {
  public component = markRaw(VHTMLBlock)

  public constructor(elem: Elem, figure: BlockFigure) {
    super(elem, figure)
    const { content, sandbox } = elem as unknown as {
      content: string
      sandbox?: string | null
    }
    this.componentProps = {
      ...this.componentProps,
      html: content,
      sandbox,
    }
  }
}

export class FormulaBlock extends Block {
  public component = markRaw(VFormulaBlock)

  public constructor(elem: Elem, figure: BlockFigure) {
    super(elem, figure)
    const content = (elem as unknown as { content: string }).content
    this.componentProps = {
      ...this.componentProps,
      content,
    }
  }
}

export class EmptyBlock extends Block {}

export class BigNumberBlock extends Block {
  public constructor(elem: Elem, figure: BlockFigure) {
    super(elem, figure)
    const {
      prevValue,
      change,
      heading,
      value,
      isPositiveIntent,
      isUpwardChange,
    } = elem as unknown as {
      prevValue?: string
      change?: string
      heading: string
      value: string
      isPositiveIntent?: boolean
      isUpwardChange?: boolean
    }
    const useSimple = !prevValue && !change
    this.component = markRaw(
      useSimple ? VBigNumberBlockSimple : VBigNumberBlock,
    )
    this.componentProps = {
      ...this.componentProps,
      heading,
      value,
    }
    if (!useSimple) {
      this.componentProps = {
        ...this.componentProps,
        isPositiveIntent: isPositiveIntent || false,
        isUpwardChange: isUpwardChange || false,
        prevValue,
        change,
      }
    }
  }
}

export class EmbedBlock extends Block {
  public component = markRaw(VEmbedBlock)

  private _isIFrame?: boolean
  private html: string

  public constructor(elem: Elem, figure: BlockFigure) {
    super(elem, figure)
    const { content } = elem as unknown as { content: string }
    this.html = content
    this.componentProps = {
      ...this.componentProps,
      html: this.html,
      isIframe: this.isIFrame,
    }
  }

  public get isIFrame(): boolean {
    /**
     * Returns `true` if the embed HTML is an iframe element
     */
    if (typeof this._isIFrame === 'undefined') {
      const doc: Document = new DOMParser().parseFromString(
        this.html,
        'text/html',
      )
      const root: HTMLBodyElement | null =
        doc.documentElement.querySelector('body')
      this._isIFrame =
        !!root &&
        root.childElementCount === 1 &&
        root.children[0].tagName.toLowerCase() === 'iframe'
    }
    return this._isIFrame
  }
}

export class SigmaBlock extends Block {
  public component = markRaw(VSigmaBlock)

  public constructor(elem: Elem, figure: BlockFigure) {
    super(elem, figure)
    const { data, layoutSettings, height, width } = elem as unknown as {
      data: unknown
      layoutSettings: unknown
      height: number
      width: number
    }
    this.componentProps = {
      ...this.componentProps,
      data,
      layoutSettings,
      height,
      width,
    }
  }
}

/* Asset blocks */

export abstract class AssetBlock extends Block {
  /**
   * Blocks whose data should be fetched on load rather than in-lined in the XML CDATA
   */
  public src: string
  public type: string

  public constructor(elem: Elem, figure: BlockFigure) {
    super(elem, figure)
    const rootStore = useRootStore()

    // Setting asset in constructor (during deserialization) as there's currently
    // no case where an existing block instance needs to have its asset dynamically updated
    const [, assetId] = (elem as unknown as { src: string }).src.split('://')

    if (!assetId) {
      throw new Error(`Couldn't get block asset ID from src ${elem.src}`)
    }

    const { src, mime } = rootStore.assetMap[assetId]
    this.src = src
    this.type = mime
    this.componentProps = {
      ...this.componentProps,
      fetchAssetData: this.fetchAssetData.bind(this),
    }
  }

  protected async fetchAssetData(): AssetResource {
    return await readGcsTextOrJsonFile(this.src)
  }
}

export class TableBlock extends AssetBlock {
  public component = markRaw(VTableBlock)
  public static captionType: CaptionType = 'Table'
}

export class FoliumBlock extends AssetBlock {
  public component = markRaw(VFoliumBlock)
  public static captionType: CaptionType = 'Plot'
}

export class AttachmentBlock extends AssetBlock {
  public component = markRaw(VAttachmentBlock)

  private readonly filename: string

  public constructor(elem: Elem, figure: BlockFigure) {
    super(elem, figure)
    const { filename } = elem as unknown as { filename: string }
    this.filename = filename
    this.componentProps = {
      ...this.componentProps,
      downloadFile: this.downloadFile.bind(this),
      filename,
    }
  }

  protected async downloadFile(): Promise<void> {
    return saveAs(this.src, this.filename)
  }
}

export class MediaBlock extends AssetBlock {
  public component = markRaw(VMediaBlock)

  public constructor(elem: Elem, figure: BlockFigure) {
    super(elem, figure)
    this.componentProps = {
      ...this.componentProps,
      type: this.type,
      src: this.src,
    }
  }
}

export abstract class PlotAssetBlock extends AssetBlock {
  public static captionType: CaptionType = 'Plot'
  public responsive: boolean

  public constructor(elem: Elem, figure: BlockFigure) {
    super(elem, figure)
    const { responsive } = elem as unknown as { responsive: boolean }
    this.responsive = responsive
    this.componentProps = {
      ...this.componentProps,
      responsive,
    }
  }
}

export class BokehBlock extends PlotAssetBlock {
  public component = markRaw(VBokehBlock)
}

export class VegaBlock extends PlotAssetBlock {
  public component = markRaw(VVegaBlock)
}

export class PlotlyBlock extends PlotAssetBlock {
  public component = markRaw(VPlotlyBlock)

  protected async fetchAssetData(): AssetResource {
    const res = await readGcsTextOrJsonFile<string>(this.src)
    return JSON.parse(res)
  }
}

export class SVGBlock extends PlotAssetBlock {
  public component = markRaw(VSVGBlock)

  protected async fetchAssetData(): AssetResource {
    return this.src
  }
}
