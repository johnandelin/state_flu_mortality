
# ---------------------------------
# Load the dataset and library
# ---------------------------------

library(tidyverse)
flu <- read_csv("influenza_pneumonia_dataset.csv")

# Preview data
head(flu)
glimpse(flu)

# ---------------------------------
# Data preprocessing
# ---------------------------------

flu <- flu |>
  mutate(year = factor(year))

# ---------------------------------
# summary stats
# ---------------------------------

summary(flu)

# ---------------------------------
# Basic visualizations
# ---------------------------------

# 1. Age-adjusted death rate vs poverty rate
flu |>
  ggplot(aes(x = poverty_rate, y = aadr)) +
  geom_point(color = "steelblue", alpha = 0.7) +
  geom_smooth(method = "lm", se = FALSE, color = "darkred") +
  labs(title = "Age-Adjusted Death Rate vs Poverty Rate",
       x = "Poverty Rate",
       y = "AADR") +
  facet_wrap(~ year) +
  theme_minimal()

# 2. States with highest and lowest AADR by year
flu |>
  group_by(year) |>
  summarise(
    max_aadr = max(aadr, na.rm = TRUE),
    max_state = state[which.max(aadr)],
    min_aadr = min(aadr, na.rm = TRUE),
    min_state = state[which.min(aadr)]
  ) |>
  print()

# 3. Histogram of AADR
flu |>
  ggplot(aes(x = aadr)) +
  geom_histogram(bins = 30, fill = "darkblue", color = "white") +
  labs(title = "Distribution of Age-Adjusted Death Rates",
       x = "AADR",
       y = "Count") +
  facet_wrap(~ year) +
  theme_minimal()

# 4. Boxplot of AADR by year
flu |>
  ggplot(aes(x = year, y = aadr)) +
  geom_boxplot(fill = "lightblue", alpha = 0.6) +
  labs(title = "Age-Adjusted Death Rate by Year",
       x = "Year",
       y = "Age-Adjusted Death Rate") +
  theme_minimal()

# ---------------------------------
# Missing values summary
# ---------------------------------
flu |>
  summarise(across(everything(), ~sum(is.na(.)))) |>
  print()
