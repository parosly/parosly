# Changelog

## 0.2.0 / 2025-01-18

* [ENHANCEMENT] The web user interface is enabled by default. It can be disabled using `--web.enable-ui=false` flag. #16
* [BUGFIX] Fixed httpx request timeout value by setting to None (never) to handle Live Notifications (/api/v1/notifications/live) that was introduced in Prometheus v3.0.0 #18
* [BUGFIX] Added `filter_external_labels` parameter in the `remote_read setting` with boolean type. #19

## 0.1.1 / 2025-01-17

* [ENHANCEMENT] Added loading indicator using pure CSS, ensuring a better user experience by providing feedback during asynchronous operations. #13 
* [BUGFIX] Fixed type definition of `remote_read` setting in the /configs API model. Added `enable_http2` property in JSON schema validation under `remote_read` setting. #11 
* [BUGFIX] Fixed favicon.ico URL in https://docs.parosly.io/ page.
* [CHANGE] Bumped [dawidd6/action-download-artifact](https://github.com/dawidd6/action-download-artifact) from 3 to 6. #1

## 0.1.0 / 2025-01-13

* [ENHANCEMENT] Initial release of Parosly, based on the [prometheus-api](https://github.com/hayk96/prometheus-api) project. The respective proposal document is available [here](https://github.com/hayk96/prometheus-api/issues/64).