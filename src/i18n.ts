import { setupI18n } from "@lingui/core"
import { catalog, DEFAULT_LOCALE, type Locale } from "./locales/catalog"

export const i18n = setupI18n({ messages: catalog })

i18n.loadAndActivate({ locale: DEFAULT_LOCALE, messages: catalog[DEFAULT_LOCALE] })

export function changeLanguage(locale: Locale): void {
    const messages = catalog[locale]
    if (!messages) return
    i18n.loadAndActivate({ locale, messages })
}
