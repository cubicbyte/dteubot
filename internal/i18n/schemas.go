package i18n

// LanguageNotFoundError is an error that is returned when
// a language with a specific language code is not found.
type LanguageNotFoundError struct {
	LangCode string
}

func (e *LanguageNotFoundError) Error() string {
	return "Language not found: " + e.LangCode
}

// Language is a struct that contains all the localization
// strings for a specific language needed for the bot.
type Language struct {
	LangName string `yaml:"lang_name"`
	Text     struct {
		Yes                 string `yaml:"yes"`
		No                  string `yaml:"no"`
		TryIt               string `yaml:"try_it"`
		NoThanks            string `yaml:"no_thanks"`
		NotSelected         string `yaml:"not_selected"`
		Unknown             string `yaml:"unknown"`
		UnknownGroupName    string `yaml:"unknown_group_name"`
		WeekDay1            string `yaml:"week_day.1"`
		WeekDay2            string `yaml:"week_day.2"`
		WeekDay3            string `yaml:"week_day.3"`
		WeekDay4            string `yaml:"week_day.4"`
		WeekDay5            string `yaml:"week_day.5"`
		WeekDay6            string `yaml:"week_day.6"`
		WeekDay7            string `yaml:"week_day.7"`
		WeekDayUnknown      string `yaml:"week_day.unknown"`
		ShortWeekDay1       string `yaml:"short_week_day.1"`
		ShortWeekDay2       string `yaml:"short_week_day.2"`
		ShortWeekDay3       string `yaml:"short_week_day.3"`
		ShortWeekDay4       string `yaml:"short_week_day.4"`
		ShortWeekDay5       string `yaml:"short_week_day.5"`
		ShortWeekDay6       string `yaml:"short_week_day.6"`
		ShortWeekDay7       string `yaml:"short_week_day.7"`
		ShortWeekDayUnknown string `yaml:"short_week_day.unknown"`
		TimeAgo             string `yaml:"time_ago"`
		TimeSeconds         string `yaml:"time.seconds"`
		TimeMinutes         string `yaml:"time.minutes"`
		TimeHours           string `yaml:"time.hours"`
		TimeDays            string `yaml:"time.days"`
		ShortTimeSeconds    string `yaml:"short_time.seconds"`
		ShortTimeMinutes    string `yaml:"short_time.minutes"`
		ShortTimeHours      string `yaml:"short_time.hours"`
		ShortTimeDays       string `yaml:"short_time.days"`
	} `yaml:"text"`
	Button struct {
		ClearCache                     string `yaml:"clear_cache"`
		GetLogs                        string `yaml:"get_logs"`
		ClearLogs                      string `yaml:"clear_logs"`
		AdminPanel                     string `yaml:"admin_panel"`
		CallsSchedule                  string `yaml:"calls_schedule"`
		TimeLeft                       string `yaml:"time_left"`
		WriteMe                        string `yaml:"write_me"`
		ClosePage                      string `yaml:"close_page"`
		Menu                           string `yaml:"menu"`
		Back                           string `yaml:"back"`
		More                           string `yaml:"more"`
		Info                           string `yaml:"info"`
		Refresh                        string `yaml:"refresh"`
		SelectGroup                    string `yaml:"select_group"`
		SelectLang                     string `yaml:"select_lang"`
		OpenSchedule                   string `yaml:"open_schedule"`
		StudentsList                   string `yaml:"students_list"`
		Settings                       string `yaml:"settings"`
		SettingClNotif15m              string `yaml:"setting.cl_notif_15m"`
		SettingClNotif1m               string `yaml:"setting.cl_notif_1m"`
		Schedule                       string `yaml:"schedule"`
		ScheduleToday                  string `yaml:"schedule.today"`
		ScheduleTomorrow               string `yaml:"schedule.tomorrow"`
		ScheduleWeek                   string `yaml:"schedule.week"`
		ScheduleNextWeek               string `yaml:"schedule.next_week"`
		ScheduleExtra                  string `yaml:"schedule.extra"`
		ScheduleNavigationToday        string `yaml:"schedule_navigation.today"`
		ScheduleNavigationNextDay      string `yaml:"schedule_navigation.next_day"`
		ScheduleNavigationNextWeek     string `yaml:"schedule_navigation.next_week"`
		ScheduleNavigationPreviousDay  string `yaml:"schedule_navigation.previous_day"`
		ScheduleNavigationPreviousWeek string `yaml:"schedule_navigation.previous_week"`
	} `yaml:"button"`
	Alert struct {
		Done                     string `yaml:"done"`
		NoPermissions            string `yaml:"no_permissions"`
		CallbackQueryUnsupported string `yaml:"callback_query_unsupported"`
		ClNotifEnabledTooltip    string `yaml:"cl_notif_enabled_tooltip"`
		MessageTooOld            string `yaml:"message_too_old"`
		FloodControl             string `yaml:"flood_control"`
	} `yaml:"alert"`
	Page struct {
		Greeting                      string `yaml:"greeting"`
		StructureSelection            string `yaml:"structure_selection"`
		FacultySelection              string `yaml:"faculty_selection"`
		CourseSelection               string `yaml:"course_selection"`
		GroupSelection                string `yaml:"group_selection"`
		InvalidGroup                  string `yaml:"invalid_group"`
		Menu                          string `yaml:"menu"`
		Settings                      string `yaml:"settings"`
		LangSelection                 string `yaml:"lang_selection"`
		More                          string `yaml:"more"`
		Info                          string `yaml:"info"`
		ApiUnavailable                string `yaml:"api_unavailable"`
		CallSchedule                  string `yaml:"call_schedule"`
		AdminPanel                    string `yaml:"admin_panel"`
		LeftToStart                   string `yaml:"left.to_start"`
		LeftToEnd                     string `yaml:"left.to_end"`
		LeftNoMore                    string `yaml:"left.no_more"`
		StudentsList                  string `yaml:"students_list"`
		ScheduleExtraInfo             string `yaml:"schedule.extra_info"`
		ScheduleEmptyDay              string `yaml:"schedule.empty_day"`
		ScheduleMultipleEmptyDays     string `yaml:"schedule.multiple_empty_days"`
		NotificationFeatureSuggestion string `yaml:"notification_feature_suggestion"`
		ClassesNotification           string `yaml:"classes_notification"`
		Error                         string `yaml:"error"`
		Forbidden                     string `yaml:"forbidden"`
		NotFound                      string `yaml:"not_found"`
	} `yaml:"page"`
}
