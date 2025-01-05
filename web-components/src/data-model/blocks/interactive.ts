import moment from 'moment'
import { markRaw } from 'vue'

import VColorField from '@/components/controls/ColorField.vue'
import VDateTimeField from '@/components/controls/DateTimeField.vue'
import VFileField from '@/components/controls/FileField.vue'
import VHiddenField from '@/components/controls/HiddenField.vue'
import VMultiChoiceField from '@/components/controls/MultiChoiceField.vue'
import VNumberBox from '@/components/controls/NumberBox.vue'
import VPasswordField from '@/components/controls/PasswordField.vue'
import VRangeField from '@/components/controls/RangeField.vue'
import VSelectField from '@/components/controls/SelectField.vue'
import VSwitchField from '@/components/controls/SwitchField.vue'
import VTagsField from '@/components/controls/TagsField.vue'
import VTextBox from '@/components/controls/TextBox.vue'

import { Block, type BlockFigure, type Elem } from './leaf-blocks'

export abstract class ControlsField extends Block {
  public constructor(elem: Elem, figure: BlockFigure) {
    super(elem, figure) // TODO -- `figure` is unused, should use new base class?
    const { name, required, initial, label, validation, help } =
      elem as unknown as {
        name: string
        required?: boolean | null
        help?: string | null
        label?: string | null
        initial?: any | null
        validation?: string | null
      }
    this.componentProps = {
      ...this.componentProps,
      name,
      label,
      initial,
      required,
      validation,
      help,
    }
  }
}

export class RangeField extends ControlsField {
  public component = markRaw(VRangeField)

  public constructor(elem: Elem, figure: BlockFigure) {
    super(elem, figure)
    const { min, max, step, initial } = elem as unknown as {
      initial: number
      min: number
      max: number
      step: number
    }
    this.componentProps = {
      ...this.componentProps,
      min: +min,
      max: +max,
      step: +step,
      initial: +initial,
    }
  }
}

export class PasswordField extends ControlsField {
  public component = markRaw(VPasswordField)
}

export class TemporalTextBox extends ControlsField {
  public component = markRaw(VTextBox)

  public constructor(elem: Elem, figure: BlockFigure, opts?: any) {
    super(elem, figure)
    const { type } = opts as { type: string }
    this.componentProps = {
      ...this.componentProps,
      type,
    }
  }
}

export class ColorField extends ControlsField {
  public component = markRaw(VColorField)
}

export class NumberBox extends ControlsField {
  public component = markRaw(VNumberBox)

  public constructor(elem: Elem, figure: BlockFigure) {
    super(elem, figure)
    const { initial } = elem as unknown as { initial?: number | null }
    this.componentProps = {
      ...this.componentProps,
      initial,
    }
  }
}

export class HiddenField extends ControlsField {
  public component = markRaw(VHiddenField)
}

export class TagsField extends ControlsField {
  public component = markRaw(VTagsField)

  public constructor(elem: Elem, figure: BlockFigure) {
    super(elem, figure)
    const { initial } = elem as unknown as { initial: string[] }
    this.componentProps = {
      ...this.componentProps,
      initial,
    }
  }
}

export class MultiChoiceField extends ControlsField {
  public component = markRaw(VMultiChoiceField)

  public constructor(elem: Elem, figure: BlockFigure) {
    super(elem, figure)
    const { initial, options } = elem as unknown as {
      initial: string[]
      options: string[]
    }
    this.componentProps = {
      ...this.componentProps,
      options,
      initial,
    }
  }
}

export class FileField extends ControlsField {
  public component = markRaw(VFileField)

  public constructor(elem: Elem, figure: BlockFigure) {
    super(elem, figure)
    const { accept } = elem as unknown as { accept?: string | null }
    this.componentProps = {
      ...this.componentProps,
      accept,
    }
  }
}

export class TemporalDateTimeField extends ControlsField {
  public component = markRaw(VDateTimeField)

  public constructor(elem: Elem, figure: BlockFigure, opts?: any) {
    super(elem, figure)
    const { initial } = elem as unknown as { initial?: string | null }
    const { timeFormat, type, parseFormat } = opts
    this.componentProps = {
      ...this.componentProps,
      // initial may be undefined -> moment() gives us current datetime
      // parseFormat may be undefined -> moment does automatic datetime parsing
      initial: (initial ? moment(initial, parseFormat) : moment()).format(
        timeFormat,
      ),
      type,
    }
  }
}

export class SelectField extends ControlsField {
  public component = markRaw(VSelectField)
  public options: string[]

  public constructor(elem: Elem, figure: BlockFigure) {
    super(elem, figure)
    const { initial, options } = elem as unknown as {
      initial?: string | null
      options: string[]
    }
    this.options = options
    this.componentProps = {
      ...this.componentProps,
      options: this.options,
      initial: initial || this.options[0],
    }
  }
}

export class SwitchField extends ControlsField {
  public component = markRaw(VSwitchField)

  public constructor(elem: Elem, figure: BlockFigure) {
    super(elem, figure)
    const { initial } = elem as unknown as { initial?: boolean | null }
    this.componentProps = {
      ...this.componentProps,
      initial,
    }
  }
}
