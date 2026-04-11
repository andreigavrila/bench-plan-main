/**
 * Schema representation for persistent storage.
 *
 * This file is a clear technical specification artifact (written in TypeScript for readability),
 * not a requirement to implement the product in TypeScript or to use any specific storage tech.
 *
 * Field names reflect one reference implementation; rebuilds may adapt names as long as
 * the product behaviors and merge rules are preserved.
 */

export type ShowType = "movie" | "tv" | "person" | "unknown";

export type MyStatusType = "active" | "next" | "later" | "done" | "quit" | "wait";

export type MyInterestType = "excited" | "interested";

export interface ProviderTypeIdLists {
  flatrate?: number[] | null;
  rent?: number[] | null;
  buy?: number[] | null;
}

export interface ProviderData {
  countries: Record<string, ProviderTypeIdLists>;
}

export interface Show {
  id: string;
  title: string;
  showType: ShowType;

  externalIds?: Record<string, string> | null;

  overview?: string | null;
  genres: string[];
  tagline?: string | null;

  homepage?: string | null;
  originalLanguage?: string | null;
  spokenLanguages: string[];
  languages: string[];

  posterUrlString?: string | null;
  backdropUrlString?: string | null;
  logoUrlString?: string | null;
  networkLogos: string[];

  voteAverage?: number | null;
  popularity?: number | null;
  voteCount?: number | null;

  lastAirDate?: string | null; // ISO-8601 date-time
  firstAirDate?: string | null; // ISO-8601 date-time
  releaseDate?: string | null; // ISO-8601 date-time

  runtime?: number | null;
  budget?: number | null;
  revenue?: number | null;

  seriesStatus?: string | null;
  numberOfEpisodes?: number | null;
  numberOfSeasons?: number | null;
  episodeRunTime: number[];
  lastEpisodeRunTime?: number | null;

  myTags: string[];
  myTagsUpdateDate?: string | null;
  myScore?: number | null;
  myScoreUpdateDate?: string | null;
  myStatus?: MyStatusType | null;
  myStatusUpdateDate?: string | null;
  myInterest?: MyInterestType | null;
  myInterestUpdateDate?: string | null;

  aiScoop?: string | null;
  aiScoopUpdateDate?: string | null;

  detailsUpdateDate?: string | null;
  creationDate?: string | null;
  isTest: boolean;

  providerData?: ProviderData | null;
}

export interface CloudSettings {
  id: string; // default "globalSettings"
  userName: string;
  version: number; // epoch seconds
  catalogApiKey?: string | null;
  aiApiKey?: string | null;
  aiModel: string; // model key/name
}

export interface AppMetadata {
  dataModelVersion: number; // default 3
}

export type FilterType =
  | "all"
  | "genre"
  | "myStatus"
  | "communityScore"
  | "decade"
  | "myTag";

export interface FilterConfiguration {
  type: FilterType;
  label: string;
  value: string;
}

export interface LocalSettings {
  autoSearch: boolean;
  fontSize: "XS" | "S" | "M" | "L" | "XL" | "XXL";
}

export interface UserDefaultsUIState {
  hideStatusRemovalConfirmation?: boolean;
  statusRemovalCountKey?: number;
  lastSelectedFilter?: FilterConfiguration | null;
}

export interface StorageSnapshot {
  shows: Show[];
  cloudSettings?: CloudSettings | null;
  appMetadata?: AppMetadata | null;
  localSettings?: LocalSettings | null;
  uiState?: UserDefaultsUIState | null;
}
