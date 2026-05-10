import { createI18n } from 'vue-i18n'
import tk from './locales/tk'
import ru from './locales/ru'

const messages = {
  tk,
  ru
}

const i18n = createI18n({
  locale: localStorage.getItem('locale') || 'tk', // set default locale
  fallbackLocale: 'ru', // set fallback locale
  messages, // set locale messages
  legacy: false // use Composition API
})

export default i18n