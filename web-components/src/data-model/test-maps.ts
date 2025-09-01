const jsonType = (json: any): string => {
  return json.type || ''
}

/* Inline blocks */

export const jsonIsMarkdown = (json: any): boolean => json._tag === 'Text'

export const jsonIsAlert = (json: any): boolean => json._tag === 'Alert'

export const jsonIsFormula = (json: any): boolean => json._tag === 'Formula'

export const jsonIsBigNumber = (json: any): boolean => json._tag === 'BigNumber'

export const jsonIsMedia = (json: any): boolean => json._tag === 'Media'

export const jsonIsHTML = (json: any): boolean => json._tag === 'HTML'

export const jsonIsCode = (json: any): boolean => json._tag === 'Code'

export const jsonIsEmbed = (json: any): boolean => json._tag === 'Embed'

export const jsonIsEmpty = (json: any): boolean => json._tag === 'Empty'

export const jsonIsAttachment = (json: any): boolean =>
  json._tag === 'Attachment'

export const jsonIsSigma = (json: any): boolean => json._tag === 'Sigma'

/* Control fields */

export const jsonIsTextBox = (json: any): boolean => json._tag === 'TextBox'

export const jsonIsURLField = (json: any): boolean => json._tag === 'URLField'

export const jsonIsEmailField = (json: any): boolean =>
  json._tag === 'EmailField'

export const jsonIsTelephoneField = (json: any): boolean =>
  json._tag === 'TelephoneField'

export const jsonIsSearchField = (json: any): boolean =>
  json._tag === 'SearchField'

export const jsonIsTextareaField = (json: any): boolean =>
  json._tag === 'TextareaField'

export const jsonIsPasswordField = (json: any): boolean =>
  json._tag === 'PasswordField'

export const jsonIsHiddenField = (json: any): boolean =>
  json._tag === 'HiddenField'

export const jsonIsColorField = (json: any): boolean =>
  json._tag === 'ColorField'

export const jsonIsNumberBox = (json: any): boolean => json._tag === 'NumberBox'

export const jsonIsRangeField = (json: any): boolean =>
  json._tag === 'RangeField'

export const jsonIsSwitchField = (json: any): boolean =>
  json._tag === 'SwitchField'

export const jsonIsTagsField = (json: any): boolean => json._tag === 'TagsField'

export const jsonIsSelectField = (json: any): boolean =>
  json._tag === 'ChoiceField'

export const jsonIsMultiChoiceField = (json: any): boolean =>
  json._tag === 'MultiChoiceField'

export const jsonIsFileField = (json: any): boolean => json._tag === 'FileField'

export const jsonIsDateTimeField = (json: any): boolean =>
  json._tag === 'DateTimeField'

export const jsonIsDateField = (json: any): boolean => json._tag === 'DateField'

export const jsonIsTimeField = (json: any): boolean => json._tag === 'TimeField'

/* Layout blocks */

export const jsonIsGroup = (json: any): boolean => json._tag === 'Group'

export const jsonIsView = (json: any): boolean => json._tag === 'View'

export const jsonIsSelect = (json: any): boolean => json._tag === 'Select'

export const jsonIsToggle = (json: any): boolean => json._tag === 'Toggle'

export const jsonIsCompute = (json: any): boolean => json._tag === 'Compute'

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
