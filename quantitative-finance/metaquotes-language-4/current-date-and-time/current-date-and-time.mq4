void OnStart() {
   datetime current_date = TimeCurrent();
   string current_date_string = TimeToStr(current_date, TIME_DATE);
   string current_time_string = TimeToStr(current_date, TIME_MINUTES|TIME_SECONDS);
   string message = "Today's date is " + current_date_string + ", and the time is " + current_time_string + ".";
   Alert(message);
}