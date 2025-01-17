# Changelog

## 0.1.1 / 2025-01-17

* [ENHANCEMENT] Added loading indicator using pure CSS, ensuring a better user experience by providing feedback during asynchronous operations. #13 
* [BUGFIX] Fixed type definition of `remote_read` setting in the /configs API model. Added `enable_http2` property in JSON schema validation under `remote_read` setting. #11 
* [BUGFIX] Fixed favicon.ico URL in https://docs.parosly.io/ page.
* [CHANGE] Bumped [dawidd6/action-download-artifact](https://github.com/dawidd6/action-download-artifact) from 3 to 6. #1

## 0.1.0 / 2025-01-13

* [ENHANCEMENT] Initial release of Parosly, based on the [prometheus-api](https://github.com/hayk96/prometheus-api) project. The respective proposal document is available [here](https://github.com/hayk96/prometheus-api/issues/64).