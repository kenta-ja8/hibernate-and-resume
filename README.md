# Hibernate and Resume
* auto hibernate by cron
  * the notification appear before hibernate
  ![hibernate-and-resume-notification](https://user-images.githubusercontent.com/50163637/132112301-45e556f5-413a-4df5-ac3a-2303c0599ce4.png)
* auto resume at 7:00


## Install
* set hibernate time and script in cron
  ```
  > crontab -u root -e
  0 22 * * * export DISPLAY=:0.0 && /xxxxx/hibernate-and-resume/hibernate-and-resume.py
  ```


## My Environment
* Manjaro (Xfce)
* Python3.9
