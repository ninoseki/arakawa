export type IReport = {
  document: any
  web_url: string
  output_is_light_prose: boolean
  output_style_header: string
  num_blocks: number
  username: string
  published: boolean
  id: string
}

export type ReportProps = {
  isLightProse: boolean
  mode: 'VIEW' | 'EMBED'
  htmlHeader: string
  report: IReport
  assetStore: any
  reportWidthClass: 'max-w-3xl' | 'max-w-screen-xl' | 'max-w-full'
  id: string
}

export type AppDataResult = {
  viewJson: any
  assets: any
}

export type AppData = {
  data: {
    result: AppDataResult
    error?: { message: string; code: number }
  }
}

export type AppMetaData = {
  isLightProse: ReportProps['isLightProse']
  mode: ReportProps['mode']
}

export enum SwapType {
  REPLACE = 'replace',
  INNER = 'inner',
  APPEND = 'append',
  PREPEND = 'prepend',
}

export enum VAlign {
  TOP = 'top',
  CENTER = 'center',
  BOTTOM = 'bottom',
}
