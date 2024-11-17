import { markRaw } from 'vue'

import VDataTableBlock from '@/components/blocks/DataTable/DataTableConnector.vue'

import {
  AssetBlock,
  type BlockFigure,
  type CaptionType,
  type Elem,
} from './index'

const AUTO_LOAD_CELLS_LIMIT = 500000

export type DatasetResponse = {
  data: any[]
  schema: any[]
  containsBigInt: boolean
}

export class DataTableBlock extends AssetBlock {
  public component = markRaw(VDataTableBlock)
  public static captionType: CaptionType = 'Table'
  public rows: number
  public columns: number
  public size: number
  public casRef: string

  private _revogridExportPlugin: any

  public get cells(): number {
    return this.rows * this.columns
  }

  public get deferLoad(): boolean {
    return this.cells > AUTO_LOAD_CELLS_LIMIT
  }

  public get exportUrl(): string {
    return this.buildExtensionUrl('export')
  }

  public constructor(elem: Elem, figure: BlockFigure) {
    super(elem, figure)
    const { attributes } = elem
    this.rows = attributes.rows
    this.columns = attributes.columns
    this.size = attributes.size
    this.casRef = attributes.cas_ref

    this.componentProps = {
      ...this.componentProps,
      streamContents: this.streamContents,
      getCsvText: this.getCsvText,
      downloadLocal: this.downloadLocal,
      deferLoad: this.deferLoad,
      cells: this.cells,
      refId: this.refId,
    }
  }

  private fetchDataset(): Promise<any> {
    return fetch(this.src).then(r => {
      if (!r.ok) {
        throw new Error('Failed to fetch dataset')
      }
      return r.arrayBuffer()
    })
  }

  public streamContents = async (): Promise<DatasetResponse> => {
    /**
     * Fetch dataset and convert to arrow format
     */
    const { apiResponseToArrow } = await import('../datatable/arrow-utils')
    const arrayBuffer = await this.fetchDataset()
    return apiResponseToArrow(arrayBuffer)
  }

  public downloadLocal = async (): Promise<void> => {
    /**
     * Download the current state of the DataTable via the client
     */
    try {
      const exportPlugin = await this.getExportPlugin()
      exportPlugin.exportFile({
        filename: `ar-export-${this.refId}`,
      })
    } catch (e) {
      console.error('An error occurred while exporting dataset: ', e)
    }
  }

  public getCsvText = async (): Promise<string> => {
    /**
     * Return dataset contents as CSV string
     */
    let csvText = ''
    try {
      const exportPlugin = await this.getExportPlugin()
      csvText = exportPlugin.exportString()
    } catch (e) {
      console.error('An error occurred while copying text to clipboard: ', e)
    }
    return csvText
  }

  private async getExportPlugin(): Promise<any> {
    /**
     * Get revogrid export plugin from its HTML element root
     */
    if (this._revogridExportPlugin) {
      return this._revogridExportPlugin
    }

    const grid = document.getElementById(
      `grid-${this.refId}`,
    ) as HTMLRevoGridElement

    if (grid) {
      const plugins = await grid.getPlugins()
      for (const p of plugins) {
        // Find export plugin by checking relevant properties
        if ((p as any).exportFile && (p as any).exportString) {
          this._revogridExportPlugin = p
          return this._revogridExportPlugin
        }
      }
    } else {
      throw 'Grid element not found'
    }
  }

  private buildExtensionUrl(name: string): string {
    return new URL(`extensions/${name}/${this.casRef}`).toString()
  }
}
