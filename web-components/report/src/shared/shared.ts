import { AxiosError } from 'axios'

export type Option = {
  name: string
  id: string
  onClick: () => void
}

export type Section = {
  title?: string
  options: Option[]
}

export const parseError = (e: unknown): string => {
  /**
   * Parse error object to be human-readable in app UI
   */
  if (e instanceof Error) {
    return e.toString()
  }
  if (typeof e === 'string') {
    return e
  }
  return 'Unable to parse error; check console for more information'
}
