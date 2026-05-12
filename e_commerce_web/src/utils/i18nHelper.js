export function getLocalized(item, field, locale) {
  if (!item) return ''
  
  // Eger saýlanan dil "tk" bolsa (default) we meýdança bar bolsa şol wagtky maglumaty gaýtarýarys.
  if (locale === 'tk' || !locale) {
    return item[field] || ''
  }

  // Eger başga dil bolsa we translations objesiň içinde şol dile degişli terjime bar bolsa
  if (item.translations && item.translations[locale] && item.translations[locale][field]) {
    return item.translations[locale][field]
  }

  // Eger terjime tapylmasa, default dildäki maglumaty gaýtarýarys.
  return item[field] || ''
}
