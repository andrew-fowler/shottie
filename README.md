### Summary

A hacky attempt at building a Saucelabs screenshotting tool

### Usage

- Enter your Saucelabs username and access key
- Enter the URL/s you'd like to hit (comma separated)
- Enter any required Webdriver commands to execute before taking the screenshot (note that these are all rooted to a remotewebdriver instance, see example code)
- Select the browser, platform and version combination you want and click Add Combination
- Repeat for as many combinations as you want
- Click Start Screenshotting to start the screenshotting jobs

After all jobs are complete the screenshot results will be shown

### TO DO

- Implement proper UI
- Open results page in new tab
- Thumbnail results 
- Display metadata for results (Browser, target URL, Saucelabs URL, etc)
- Allow .zip download of all screenshots
- Remember users job combination requests
- Show a Job History list
- Allow user to re-fire jobs from the History list
- Implement custom webdriver wrapper to sanitize command inputs

### DONE

- Allow user to (optionally) provide webdriver interaction commands, to execute before screenshot fires
- Parallelize screenshot jobs