# Usage

-   Create and ENV!!
    ```powershell
    python3 -m venv env
    python3 -m venv [env_name]
    ```
-   Activate the env while in the directory where the project is
    ```powershell
    source [env_name]/bin/activate
    ```
-   Install packages from the requirements.txt
    ```powershell
    pip3 install -r requirements.txt
    ```
-   navigate to [.src/config.py](./src/config.py) to change the number of accounts

    ```python
    config = {
      "number_of_accounts_to_generate": 10
    }
    ```

### now for the hard part 🙂

-   navigate to

    ```powershell
    [env_name]/lib/python3.10/site-packages/bose/download_driver.py
    ```

    and update the function `def download_driver():` to the following

    ```python
    def download_driver():
      build_dir = "build"

      if not os.path.exists(build_dir):
          os.makedirs(build_dir)

      major_version = get_major_version(get_chrome_version())
      print(f'[INFO] Downloading Driver for Chrome Version {major_version} in {build_dir}/ directory. This is a one-time process. Download in progress...')

      download_driver_in_path()
      move_driver()
    ```

that should fix any errors you might have concerning downloading of a driver for `chrome version 115` or above

### download a chrome driver

Note: `The chrome driver version you download should be the same as your chrome version` which you can check here [chrome://settings/help](chrome://settings/help)

My chrome version is `115.0.5790.170` and i use a Linux so i head on to here: https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/115.0.5790.170/linux64/chromedriver-linux64.zip
to download a driver

After you're done hopefully inside build create a folder named the `Major version` of your chrome in my case it would be `build/115` then add the chromedriver to it making it `build/115/chromedriver`

That's all, note this is if you encounter an issue like this

```shell
(env) rafe@shadrach:~/codes/git codes/outlook-account-generator$ python main.py
Task Started
[INFO] Downloading Driver for Chrome Version 115 in build/ directory. This is a one-time process. Download in progress...
WARNING:root:Can not find chromedriver for currently installed chrome version.
Traceback (most recent call last):
  File "/usr/lib/python3.10/shutil.py", line 815, in move
    os.rename(src, real_dst)
FileNotFoundError: [Errno 2] No such file or directory: 'build/115/chromedriver' -> 'build/chromedriver'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/rafe/codes/git codes/outlook-account-generator/main.py", line 5, in <module>
    launch_tasks(*tasks_to_be_run)
  File "/home/rafe/codes/git codes/outlook-account-generator/env/lib/python3.10/site-packages/bose/launch_tasks.py", line 54, in launch_tasks
    current_output = task.begin_task(current_data, task_config)
  File "/home/rafe/codes/git codes/outlook-account-generator/env/lib/python3.10/site-packages/bose/base_task.py", line 214, in begin_task
    final = run_task(False, 0)
  File "/home/rafe/codes/git codes/outlook-account-generator/env/lib/python3.10/site-packages/bose/base_task.py", line 155, in run_task
    create_directories(self.task_path)
  File "/home/rafe/codes/git codes/outlook-account-generator/env/lib/python3.10/site-packages/bose/base_task.py", line 99, in create_directories
    _download_driver()
  File "/home/rafe/codes/git codes/outlook-account-generator/env/lib/python3.10/site-packages/bose/base_task.py", line 34, in _download_driver
    download_driver()
  File "/home/rafe/codes/git codes/outlook-account-generator/env/lib/python3.10/site-packages/bose/download_driver.py", line 50, in download_driver
    move_driver()
  File "/home/rafe/codes/git codes/outlook-account-generator/env/lib/python3.10/site-packages/bose/download_driver.py", line 39, in move_driver
    move_chromedriver()
  File "/home/rafe/codes/git codes/outlook-account-generator/env/lib/python3.10/site-packages/bose/download_driver.py", line 38, in move_chromedriver
    shutil.move(src_path, dest_path)
  File "/usr/lib/python3.10/shutil.py", line 835, in move
    copy_function(src, real_dst)
  File "/usr/lib/python3.10/shutil.py", line 434, in copy2
    copyfile(src, dst, follow_symlinks=follow_symlinks)
  File "/usr/lib/python3.10/shutil.py", line 254, in copyfile
    with open(src, 'rb') as fsrc:
FileNotFoundError: [Errno 2] No such file or directory: 'build/115/chromedriver'

```
