import datetime
from dataclasses import dataclass


@dataclass
class OuraDailyActivityContributors:
    meet_daily_targets: int
    move_every_hour: int
    recovery_time: int
    stay_active: int
    training_frequency: int
    training_volume: int


@dataclass
class OuraDailyActivityMet:
    interval: float
    items: list[float]
    timestamp: datetime.datetime | None


@dataclass
class OuraDailyActivity:
    id: str | None
    class_5_min: str
    score: int
    active_calories: int
    average_met_minutes: float
    contributors: OuraDailyActivityContributors
    equivalent_walking_distance: int
    high_activity_met_minutes: int
    high_activity_time: int
    inactivity_alerts: int
    low_activity_met_minutes: int
    low_activity_time: int
    medium_activity_met_minutes: int
    medium_activity_time: int
    met: OuraDailyActivityMet
    meters_to_target: int
    non_wear_time: int
    resting_time: int
    sedentary_met_minutes: int
    sedentary_time: int
    steps: int
    target_calories: int
    target_meters: int
    total_calories: int
    day: datetime.date
    timestamp: datetime.datetime | None


@dataclass
class OuraDailyActivities:
    data: list[OuraDailyActivity]
    next_token: str | None


@dataclass
class OuraDailyReadinessContributors:
    activity_balance: int
    body_temperature: int
    hrv_balance: int | None
    previous_day_activity: int
    previous_night: int
    recovery_index: int
    resting_heart_rate: int
    sleep_balance: int


@dataclass
class OuraDailyReadiness:
    id: str | None
    contributors: OuraDailyReadinessContributors
    day: datetime.date
    score: int
    temperature_deviation: float
    temperature_trend_deviation: float
    timestamp: datetime.datetime | None


@dataclass
class OuraDailyReadinesses:
    data: list[OuraDailyReadiness]
    next_token: str | None


@dataclass
class OuraDailyResilienceContributors:
    sleep_recovery: float
    daytime_recovery: float
    stress: float


@dataclass
class OuraDailyResilience:
    id: str | None
    contributors: OuraDailyResilienceContributors
    day: datetime.date
    level: str


@dataclass
class OuraDailyResiliences:
    data: list[OuraDailyResilience]
    next_token: str | None


@dataclass
class OuraDailySleepContributors:
    deep_sleep: int
    efficiency: int
    latency: int
    rem_sleep: int
    restfulness: int
    timing: int
    total_sleep: int


@dataclass
class OuraDailySleep:
    id: str | None
    contributors: OuraDailySleepContributors
    day: datetime.date
    score: int
    timestamp: datetime.datetime | None


@dataclass
class OuraDailySleeps:
    data: list[OuraDailySleep]
    next_token: str | None


@dataclass
class OuraDailySpo2Spo2Percentage:
    average: float


@dataclass
class OuraDailySpo2:
    id: str | None
    day: datetime.date
    spo2_percentage: OuraDailySpo2Spo2Percentage | None


@dataclass
class OuraDailySpo2s:
    data: list[OuraDailySpo2]
    next_token: str | None


@dataclass
class OuraDailyStress:
    id: str | None
    day: datetime.date
    stress_high: int | None
    recovery_high: int | None
    day_summary: str | None


@dataclass
class OuraDailyStresses:
    data: list[OuraDailyStress]
    next_token: str | None


@dataclass
class OuraHeartRate:
    bpm: int
    source: str
    timestamp: datetime.datetime | None


@dataclass
class OuraHeartRates:
    data: list[OuraHeartRate]
    next_token: str | None


@dataclass
class OuraSleepHeartRateData:
    interval: float
    items: list
    timestamp: datetime.datetime | None


@dataclass
class OuraSleepHRVData:
    interval: float
    items: list
    timestamp: datetime.datetime | None


@dataclass
class OuraSleepReadinessContributors:
    activity_balance: int | None
    body_temperature: int | None
    hrv_balance: int | None
    previous_day_activity: int | None
    previous_night: int | None
    recovery_index: int | None
    resting_heart_rate: int | None
    sleep_balance: int | None


@dataclass
class OuraSleepReadiness:
    contributors: OuraSleepReadinessContributors
    score: int | None
    temperature_deviation: float | None
    temperature_trend_deviation: float | None


@dataclass
class OuraPersonalInfo:
    id: str | None
    age: int
    weight: float
    height: float
    biological_sex: str
    email: str


@dataclass
class OuraRestModePeriod:
    id: str | None
    start_datetime: datetime.datetime | None
    end_datetime: datetime.datetime | None
    timestamp: datetime.datetime | None


@dataclass
class OuraRestModePeriods:
    data: list[OuraRestModePeriod]
    next_token: str | None


@dataclass
class OuraRingConfiguration:
    id: str | None
    battery_level: int | None
    device_type: str | None
    firmware_version: str | None
    hardware_revision: str | None
    timestamp: datetime.datetime | None | None


@dataclass
class OuraRingConfigurations:
    data: list[OuraRingConfiguration]
    next_token: str | None


@dataclass
class OuraSession:
    id: str | None
    day: datetime.date | None
    start_datetime: datetime.datetime | None
    end_datetime: datetime.datetime | None
    type: str | None
    heart_rate: OuraHeartRate | None
    motion_count: int | None
    timestamp: datetime.datetime | None


@dataclass
class OuraSessions:
    data: list[OuraSession]
    next_token: str | None


@dataclass
class OuraSleepPhase:
    phase: str | None
    start_time: datetime.datetime | None
    end_time: datetime.datetime | None
    duration_ms: int | None


@dataclass
class OuraSleepMovement:
    start_time: datetime.datetime | None
    end_time: datetime.datetime | None
    activity_level: float | None
    duration_ms: int | None


@dataclass
class OuraSleep:
    id: str
    average_breath: float | None
    average_heart_rate: float | None
    average_hrv: int | None
    awake_time: int | None
    bedtime_end: datetime.datetime | None
    bedtime_start: datetime.datetime | None
    day: datetime.date | None
    deep_sleep_duration: int | None
    efficiency: int | None
    heart_rate: OuraSleepHeartRateData | None
    hrv: OuraSleepHRVData | None
    latency: int | None
    light_sleep_duration: int | None
    low_battery_alert: bool | None
    lowest_heart_rate: int | None
    movement_30_sec: str | None
    period: int | None
    readiness: OuraSleepReadiness | None
    readiness_score_delta: float | None
    rem_sleep_duration: int | None
    restless_periods: int | None
    ring_id: str | None
    sleep_phase_5_min: str | None
    sleep_score_delta: float | None
    sleep_algorithm_version: str | None
    sleep_analysis_reason: str | None
    time_in_bed: int | None
    total_sleep_duration: int | None
    type: str | None


@dataclass
class OuraSleeps:
    data: list[OuraSleep]
    next_token: str | None


@dataclass
class OuraSleepTime:
    id: str | None
    bedtime_end_delta: int | None
    bedtime_start_delta: int | None
    day: datetime.date | None
    ideal_bedtime: str | None
    is_longest: bool | None
    midpoint_time: int | None
    timestamp: datetime.datetime | None | None


@dataclass
class OuraSleepTimes:
    data: list[OuraSleepTime]
    next_token: str | None


@dataclass
class OuraTag:
    id: str | None
    day: datetime.date | None
    start_datetime: datetime.datetime | None
    end_datetime: datetime.datetime | None
    tag_type_code: int | None
    text: str | None
    timestamp: datetime.datetime | None


@dataclass
class OuraTags:
    data: list[OuraTag]
    next_token: str | None


@dataclass
class OuraVO2Max:
    id: str | None
    vo2_max: float | None
    day: datetime.date
    timestamp: datetime.datetime | None


@dataclass
class OuraVO2Maxes:
    data: list[OuraVO2Max]
    next_token: str | None


@dataclass
class OuraWorkoutHeartRate:
    start_datetime: datetime.datetime | None
    end_datetime: datetime.datetime | None
    heart_rate: int | None


@dataclass
class OuraWorkoutIntensity:
    start_datetime: datetime.datetime | None
    end_datetime: datetime.datetime | None
    met_value: float | None


@dataclass
class OuraWorkout:
    id: str | None
    activity: str | None
    calories: int | None
    day: datetime.date | None
    distance: int | None
    end_datetime: datetime.datetime | None
    heart_rate: list[OuraWorkoutHeartRate] | None
    intensity: list[OuraWorkoutIntensity] | None
    max_heart_rate: int | None
    start_datetime: datetime.datetime | None
    timestamp: datetime.datetime | None


@dataclass
class OuraWorkouts:
    data: list[OuraWorkout]
    next_token: str | None


@dataclass
class OuraEnhancedTag:
    id: str | None
    day: datetime.date | None
    start_datetime: datetime.datetime | None
    end_datetime: datetime.datetime | None
    tag_type_code: int | None
    text: str | None
    timestamp: datetime.datetime | None
    metadata: dict | None


@dataclass
class OuraEnhancedTags:
    data: list[OuraEnhancedTag]
    next_token: str | None
