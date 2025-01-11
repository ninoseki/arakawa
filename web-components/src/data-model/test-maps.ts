const jsonType = (json: any): string => {
  return json.type || ''
}

/* Inline blocks */

export const jsonIsMarkdown = (json: any): boolean => json._type === 'Text'

export const jsonIsFormula = (json: any): boolean => json._type === 'Formula'

export const jsonIsBigNumber = (json: any): boolean =>
  json._type === 'BigNumber'

export const jsonIsMedia = (json: any): boolean => json._type === 'Media'

export const jsonIsHTML = (json: any): boolean => json._type === 'HTML'

export const jsonIsCode = (json: any): boolean => json._type === 'Code'

export const jsonIsEmbed = (json: any): boolean => json._type === 'Embed'

export const jsonIsEmpty = (json: any): boolean => json._type === 'Empty'

export const jsonIsAttachment = (json: any): boolean =>
  json._type === 'Attachment'

/* Control fields */

export const jsonIsTextBox = (json: any): boolean => json._type === 'TextBox'

export const jsonIsURLField = (json: any): boolean => json._type === 'URLField'

export const jsonIsEmailField = (json: any): boolean =>
  json._type === 'EmailField'

export const jsonIsTelephoneField = (json: any): boolean =>
  json._type === 'TelephoneField'

export const jsonIsSearchField = (json: any): boolean =>
  json._type === 'SearchField'

export const jsonIsTextareaField = (json: any): boolean =>
  json._type === 'TextareaField'

export const jsonIsPasswordField = (json: any): boolean =>
  json._type === 'PasswordField'

export const jsonIsHiddenField = (json: any): boolean =>
  json._type === 'HiddenField'

export const jsonIsColorField = (json: any): boolean =>
  json._type === 'ColorField'

export const jsonIsNumberBox = (json: any): boolean =>
  json._type === 'NumberBox'

export const jsonIsRangeField = (json: any): boolean =>
  json._type === 'RangeField'

export const jsonIsSwitchField = (json: any): boolean =>
  json._type === 'SwitchField'

export const jsonIsTagsField = (json: any): boolean =>
  json._type === 'TagsField'

export const jsonIsSelectField = (json: any): boolean =>
  json._type === 'ChoiceField'

export const jsonIsMultiChoiceField = (json: any): boolean =>
  json._type === 'MultiChoiceField'

export const jsonIsFileField = (json: any): boolean =>
  json._type === 'FileField'

export const jsonIsDateTimeField = (json: any): boolean =>
  json._type === 'DateTimeField'

export const jsonIsDateField = (json: any): boolean =>
  json._type === 'DateField'

export const jsonIsTimeField = (json: any): boolean =>
  json._type === 'TimeField'

/* Layout blocks */

export const jsonIsGroup = (json: any): boolean => json._type === 'Group'

export const jsonIsView = (json: any): boolean => json._type === 'View'

export const jsonIsSelect = (json: any): boolean => json._type === 'Select'

export const jsonIsToggle = (json: any): boolean => json._type === 'Toggle'

export const jsonIsCompute = (json: any): boolean => json._type === 'Compute'

/* Asset blocks */

export const jsonIsVega = (json: any): boolean =>
  jsonType(json).includes('application/vnd.vegalite')

export const jsonIsArrowTable = (json: any): boolean =>
  jsonType(json).includes('application/vnd.apache.arrow+binary')

export const jsonIsHTMLTable = (json: any): boolean =>
  jsonType(json) === 'application/vnd.arakawa.table+html'

export const jsonIsIFrameHTML = (json: any): boolean =>
  jsonType(json) === 'application/vnd.folium+html'

export const jsonIsBokeh = (json: any): boolean =>
  jsonType(json) === 'application/vnd.bokeh.show+json'

export const jsonIsPlotly = (json: any): boolean =>
  jsonType(json) === 'application/vnd.plotly.v1+json'

export const jsonIsSvg = (json: any): boolean =>
  jsonType(json).includes('image/svg')
