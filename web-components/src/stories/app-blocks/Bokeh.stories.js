import Bokeh from '@/components/blocks/Bokeh.vue'

import { makeTemplate } from '../utils'

export default {
  title: 'Bokeh',
  component: Bokeh,
}

export const Primary = makeTemplate(Bokeh)

// Generated from Bokeh 3.9.0 via `bokeh.embed.json_item(figure)` —
// regenerate when bumping `@bokeh/bokehjs` to keep the schema in sync.
Primary.args = {
  responsive: true,
  plotJson: {
    target_id: null,
    root_id: 'p1006',
    doc: {
      version: '3.9.0',
      title: '',
      config: {
        type: 'object',
        name: 'DocumentConfig',
        id: 'p1052',
        attributes: {
          notifications: { type: 'object', name: 'Notifications', id: 'p1053' },
        },
      },
      roots: [
        {
          type: 'object',
          name: 'Figure',
          id: 'p1006',
          attributes: {
            x_range: { type: 'object', name: 'DataRange1d', id: 'p1007' },
            y_range: { type: 'object', name: 'DataRange1d', id: 'p1008' },
            x_scale: { type: 'object', name: 'LinearScale', id: 'p1016' },
            y_scale: { type: 'object', name: 'LinearScale', id: 'p1017' },
            title: {
              type: 'object',
              name: 'Title',
              id: 'p1009',
              attributes: { text: 'simple line example' },
            },
            renderers: [
              {
                type: 'object',
                name: 'GlyphRenderer',
                id: 'p1047',
                attributes: {
                  data_source: {
                    type: 'object',
                    name: 'ColumnDataSource',
                    id: 'p1041',
                    attributes: {
                      selected: {
                        type: 'object',
                        name: 'Selection',
                        id: 'p1042',
                        attributes: { indices: [], line_indices: [] },
                      },
                      selection_policy: {
                        type: 'object',
                        name: 'UnionRenderers',
                        id: 'p1043',
                      },
                      data: {
                        type: 'map',
                        entries: [
                          ['x', [1, 2, 3, 4, 5]],
                          ['y', [6, 7, 2, 4, 5]],
                        ],
                      },
                    },
                  },
                  view: {
                    type: 'object',
                    name: 'CDSView',
                    id: 'p1048',
                    attributes: {
                      filter: { type: 'object', name: 'AllIndices', id: 'p1049' },
                    },
                  },
                  glyph: {
                    type: 'object',
                    name: 'Line',
                    id: 'p1044',
                    attributes: {
                      x: { type: 'field', field: 'x' },
                      y: { type: 'field', field: 'y' },
                      line_color: '#1f77b4',
                      line_width: 2,
                    },
                  },
                  nonselection_glyph: {
                    type: 'object',
                    name: 'Line',
                    id: 'p1045',
                    attributes: {
                      x: { type: 'field', field: 'x' },
                      y: { type: 'field', field: 'y' },
                      line_color: '#1f77b4',
                      line_alpha: 0.1,
                      line_width: 2,
                    },
                  },
                  muted_glyph: {
                    type: 'object',
                    name: 'Line',
                    id: 'p1046',
                    attributes: {
                      x: { type: 'field', field: 'x' },
                      y: { type: 'field', field: 'y' },
                      line_color: '#1f77b4',
                      line_alpha: 0.2,
                      line_width: 2,
                    },
                  },
                },
              },
            ],
            toolbar: {
              type: 'object',
              name: 'Toolbar',
              id: 'p1015',
              attributes: {
                tools: [
                  { type: 'object', name: 'PanTool', id: 'p1028' },
                  {
                    type: 'object',
                    name: 'WheelZoomTool',
                    id: 'p1029',
                    attributes: { renderers: 'auto' },
                  },
                  {
                    type: 'object',
                    name: 'BoxZoomTool',
                    id: 'p1030',
                    attributes: {
                      overlay: {
                        type: 'object',
                        name: 'BoxAnnotation',
                        id: 'p1031',
                        attributes: {
                          syncable: false,
                          line_color: 'black',
                          line_alpha: 1.0,
                          line_width: 2,
                          line_dash: [4, 4],
                          fill_color: 'lightgrey',
                          fill_alpha: 0.5,
                          level: 'overlay',
                          visible: false,
                          left: { type: 'number', value: 'nan' },
                          right: { type: 'number', value: 'nan' },
                          top: { type: 'number', value: 'nan' },
                          bottom: { type: 'number', value: 'nan' },
                          left_units: 'canvas',
                          right_units: 'canvas',
                          top_units: 'canvas',
                          bottom_units: 'canvas',
                          handles: {
                            type: 'object',
                            name: 'BoxInteractionHandles',
                            id: 'p1037',
                            attributes: {
                              all: {
                                type: 'object',
                                name: 'AreaVisuals',
                                id: 'p1036',
                                attributes: {
                                  fill_color: 'white',
                                  hover_fill_color: 'lightgray',
                                },
                              },
                            },
                          },
                        },
                      },
                    },
                  },
                  { type: 'object', name: 'SaveTool', id: 'p1038' },
                  { type: 'object', name: 'ResetTool', id: 'p1039' },
                  { type: 'object', name: 'HelpTool', id: 'p1040' },
                ],
              },
            },
            left: [
              {
                type: 'object',
                name: 'LinearAxis',
                id: 'p1023',
                attributes: {
                  ticker: {
                    type: 'object',
                    name: 'BasicTicker',
                    id: 'p1024',
                    attributes: { mantissas: [1, 2, 5] },
                  },
                  formatter: {
                    type: 'object',
                    name: 'BasicTickFormatter',
                    id: 'p1025',
                  },
                  axis_label: 'y',
                  major_label_policy: { type: 'object', name: 'AllLabels', id: 'p1026' },
                },
              },
            ],
            below: [
              {
                type: 'object',
                name: 'LinearAxis',
                id: 'p1018',
                attributes: {
                  ticker: {
                    type: 'object',
                    name: 'BasicTicker',
                    id: 'p1019',
                    attributes: { mantissas: [1, 2, 5] },
                  },
                  formatter: {
                    type: 'object',
                    name: 'BasicTickFormatter',
                    id: 'p1020',
                  },
                  axis_label: 'x',
                  major_label_policy: { type: 'object', name: 'AllLabels', id: 'p1021' },
                },
              },
            ],
            center: [
              {
                type: 'object',
                name: 'Grid',
                id: 'p1022',
                attributes: { axis: { id: 'p1018' } },
              },
              {
                type: 'object',
                name: 'Grid',
                id: 'p1027',
                attributes: { dimension: 1, axis: { id: 'p1023' } },
              },
              {
                type: 'object',
                name: 'Legend',
                id: 'p1050',
                attributes: {
                  items: [
                    {
                      type: 'object',
                      name: 'LegendItem',
                      id: 'p1051',
                      attributes: {
                        label: { type: 'value', value: 'Temp.' },
                        renderers: [{ id: 'p1047' }],
                      },
                    },
                  ],
                },
              },
            ],
          },
        },
      ],
    },
    version: '3.9.0',
  },
}
