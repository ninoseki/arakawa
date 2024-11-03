import ClipboardJS from 'clipboard'

type ClipboardOptions = {
  text?: string
  fieldId?: string
}
type CopyBtn = string | Element | NodeListOf<Element>

export class ARClipboard {
  /**
   * Clipboard API that binds a clipboard write event to supplied button element,
   * and shows a notification on copy
   */
  private clip: ClipboardJS

  public constructor(btn: CopyBtn, options: ClipboardOptions) {
    /**
     * btn: The button to bind the copy action to
     * options: Either the raw text to write to clipboard, or the input field whose value should be used
     */
    this.clip = new ClipboardJS(btn, {
      text() {
        const textToCopy = options.text
          ? options.text
          : ARClipboard.getFieldValue(options.fieldId)
        return textToCopy
      },
    })
    this.clip.on('error', () =>
      console.error('An error occurred while copying to clipboard'),
    )
    this.clip.on('success', ARClipboard.onSuccess)
  }

  public destroy() {
    this.clip.destroy()
  }

  private static onSuccess = () => {
    const notificationEl = document.getElementById('copy-notification')
    if (notificationEl) {
      notificationEl.classList.toggle('ar-invisible')
      setTimeout(() => notificationEl.classList.toggle('ar-invisible'), 2000)
    }
  }

  private static getFieldValue(fieldId?: string): string {
    const field = document.querySelector<HTMLInputElement>(`#${fieldId}`)

    if (!field) {
      throw `Field with ID ${fieldId} not found`
    }

    return field.value
  }

  public static async copyOnce(text: string): Promise<void> {
    /**
     * Copy on the fly using the native `navigator` API -- useful in cases where it's inefficient to use Clipboard.js
     * as it requires maintaining the text in memory before copying is triggered via a listener.
     *
     * Note that in Firefox and Safari this method will only work if part of a user action callback (e.g. button.onClick)
     */
    try {
      await navigator.clipboard.writeText(text)
      ARClipboard.onSuccess()
    } catch (e) {
      console.error('Error copying to clipboard: ', e)
    }
  }
}
