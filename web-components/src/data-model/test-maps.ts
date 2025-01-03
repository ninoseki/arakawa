const jsonType = (json: any): string => {
  return json.type || ''
}

/* Inline blocks */

export const jsonIsMarkdown = (json: any): boolean => json._id === 'Text'

export const jsonIsFormula = (json: any): boolean => json._id === 'Formula'

export const jsonIsBigNumber = (json: any): boolean => json._id === 'BigNumber'

export const jsonIsMedia = (json: any): boolean => json._id === 'Media'

export const jsonIsHTML = (json: any): boolean => json._id === 'HTML'

export const jsonIsCode = (json: any): boolean => json._id === 'Code'

export const jsonIsEmbed = (json: any): boolean => json._id === 'Embed'

export const jsonIsEmpty = (json: any): boolean => json._id === 'Empty'

export const jsonIsAttachment = (json: any): boolean =>
  json._id === 'Attachment'

/* Control fields */

export const jsonIsTextBox = (json: any): boolean => json._id === 'TextBox'

export const jsonIsURLField = (json: any): boolean => json._id === 'URLField'

export const jsonIsEmailField = (json: any): boolean =>
  json._id === 'EmailField'

export const jsonIsTelephoneField = (json: any): boolean =>
  json._id === 'TelephoneField'

export const jsonIsSearchField = (json: any): boolean =>
  json._id === 'SearchField'

export const jsonIsTextareaField = (json: any): boolean =>
  json._id === 'TextareaField'

export const jsonIsPasswordField = (json: any): boolean =>
  json._id === 'PasswordField'

export const jsonIsHiddenField = (json: any): boolean =>
  json._id === 'HiddenField'

export const jsonIsColorField = (json: any): boolean =>
  json._id === 'ColorField'

export const jsonIsNumberBox = (json: any): boolean => json._id === 'NumberBox'

export const jsonIsRangeField = (json: any): boolean =>
  json._id === 'RangeField'

export const jsonIsSwitchField = (json: any): boolean =>
  json._id === 'SwitchField'

export const jsonIsTagsField = (json: any): boolean => json._id === 'TagsField'

export const jsonIsSelectField = (json: any): boolean =>
  json._id === 'ChoiceField'

export const jsonIsMultiChoiceField = (json: any): boolean =>
  json._id === 'MultiChoiceField'

export const jsonIsFileField = (json: any): boolean => json._id === 'FileField'

export const jsonIsDateTimeField = (json: any): boolean =>
  json._id === 'DateTimeField'

export const jsonIsDateField = (json: any): boolean => json._id === 'DateField'

export const jsonIsTimeField = (json: any): boolean => json._id === 'TimeField'

/* Layout blocks */

export const jsonIsGroup = (json: any): boolean => json._id === 'Group'

export const jsonIsView = (json: any): boolean => json._id === 'View'

export const jsonIsSelect = (json: any): boolean => json._id === 'Select'

export const jsonIsToggle = (json: any): boolean => json._id === 'Toggle'

export const jsonIsCompute = (json: any): boolean => json._id === 'Compute'

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
