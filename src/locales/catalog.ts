import { messages as en } from "./en/messages.mjs"
import { messages as zh_Hans } from "./zh-Hans/messages.mjs"

export const catalog = {
    "zh-Hans": zh_Hans,
    en,
} as const

export type Locale = keyof typeof catalog

export const DEFAULT_LOCALE: Locale = "zh-Hans"
