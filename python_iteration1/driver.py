from ZoomPollAnalyzer import ZoomPollAnalyzer

driver = ZoomPollAnalyzer("answer-keys-directory", "students-list-directory", "polls-directory", "output")
driver.start()
