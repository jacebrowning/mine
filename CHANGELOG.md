# Revision History

## 1.1 (unreleased)

- Updated `switch` to close all locally running applications.

## 1.0 (2016/11/01)

- Initial stable release.

## 0.6.1 (2016/09/23)

- Added a delay to ensure all applications close.
- Fixed cleanup of unused applications and computers.

## 0.6 (2016/07/02)

- Added a `close` command to close all locally running applications.

## 0.5 (2016/05/16)

- Added periodic checking to the daemon (regardless of file changes).

## 0.4.3 (2016/05/11)

- Fixed `__init__` warnings with YORM v0.8.1.

## 0.4.2 (2016/03/30)

- Updated to YORM v0.7.2.

## 0.4.1 (2016/02/23)

- Updated to YORM v0.6.

## 0.4 (2015/12/30)

- Added file watching to update program state faster.

## 0.3 (2015/11/14)

- Added automatic daemon restart using `nohup`.
- Moved `queued` to setting `properties.single_instance`.
- Added `properties.auto_queue` to filter active applications.

## 0.2.1 (2015/09/05)

- Fixed daemon warning to run using `nohup`

## 0.2 (2015/08/27)

- Added `--daemon` option to run continuously.
- Added `edit` command to launch the settings file.

## 0.1.2 (2015/05/17)

- Updated to YORM v0.4.

## 0.1.1 (2015/03/19)

 - Initial release.
