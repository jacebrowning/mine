# Release Notes

## 4.2 (2023-07-23)

- Added `keep_running` option for applications that can stay running forever.

## 4.1 (2023-07-22)

- Added a flag to manually stop the background daemon process.
- Added a flag to reset the internal status counter.
- Improved change detection in the daemon loop.

## 4.0 (2023-07-20)

- Dropped support for Python 3.8 and 3.9.
- Improved computer identification using serial numbers.

## 3.1.1 (2023-07-15)

- Updated logic to save missing serial numbers.

## 3.1 (2023-07-14)

- Use serial numbers as another way to identify computers.

## 3.0.1 (2023-04-16)

- Updated dependencies.

## 3.0 (2023-04-15)

- Dropped support for Python 3.7.
- Updated computer matching to prefer exact matches over partials.

## 2.0 (2022-08-16)

- Dropped support for Python 3.6.

## 1.8 (2020-05-16)

- Added a delay to the daemon to wait for files to finish synching.

## 1.7 (2020-02-01)

- Updated search to find common macOS applications before local.

## 1.6.1 (2019-10-14)

- Added support for "/System/Applications" in macOS Catalina.

## 1.6 (2019-05-20)

- Ignored conflicting program name ("garcon.appex").

## 1.5 (2017-10-22)

- Ignored conflicting program name ("slack helper.app").

## 1.4 (2017-04-18)

- Added color to display the state of running applications.
- Dropped support for Python 3.3, 3.4, and 3.5.

## 1.3 (2017-03-13)

- Ignored conflicting program name ("iTunes Helper.app").

## 1.2 (2017-02-13)

- Restart Dropbox automatically.

## 1.1 (2017-01-07)

- Updated `switch` to close all locally running applications.

## 1.0 (2016-11-01)

- Initial stable release.

## 0.6.1 (2016-09-23)

- Added a delay to ensure all applications close.
- Fixed cleanup of unused applications and computers.

## 0.6 (2016-07-02)

- Added a `close` command to close all locally running applications.

## 0.5 (2016-05-16)

- Added periodic checking to the daemon (regardless of file changes).

## 0.4.3 (2016-05-11)

- Fixed `__init__` warnings with YORM v0.8.1.

## 0.4.2 (2016-03-30)

- Updated to YORM v0.7.2.

## 0.4.1 (2016-02-23)

- Updated to YORM v0.6.

## 0.4 (2015-12-30)

- Added file watching to update program state faster.

## 0.3 (2015-11-14)

- Added automatic daemon restart using `nohup`.
- Moved `queued` to setting `properties.single_instance`.
- Added `properties.auto_queue` to filter active applications.

## 0.2.1 (2015-09-05)

- Fixed daemon warning to run using `nohup`

## 0.2 (2015-08-27)

- Added `--daemon` option to run continuously.
- Added `edit` command to launch the settings file.

## 0.1.2 (2015-05-17)

- Updated to YORM v0.4.

## 0.1.1 (2015-03-19)

- Initial release.
