import customtkinter as ctk
from tkinter import messagebox
from aliyunsdkcore.client import AcsClient
from aliyunsdkcdn.request.v20180510.RefreshObjectCachesRequest import (
    RefreshObjectCachesRequest,
)
import json
import threading
from dotenv import load_dotenv, set_key
import os

HISTORY_FILE = "path_history.txt"
ENV_FILE = ".env"
load_dotenv()


# 初始化主题
ctk.set_default_color_theme("blue")
ctk.set_appearance_mode("System")


class CDNRefreshApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("阿里云 CDN 刷新工具")
        self.geometry("600x750")

        # Access Key 配置
        self.label_id = ctk.CTkLabel(self, text="AccessKey ID:")
        self.label_id.pack(pady=(10, 0))
        self.entry_id = ctk.CTkEntry(self, width=550)
        self.entry_id.pack(pady=5)

        self.label_secret = ctk.CTkLabel(self, text="AccessKey Secret:")
        self.label_secret.pack(pady=(10, 0))
        self.entry_secret = ctk.CTkEntry(self, width=550, show="*")
        self.entry_secret.pack(pady=5)

        # 自动填充 AccessKey
        self.entry_id.insert(0, os.getenv("ACCESS_KEY_ID", ""))
        self.entry_secret.insert(0, os.getenv("ACCESS_KEY_SECRET", ""))

        self.button_save_key = ctk.CTkButton(
            self, text="保存 AccessKey 到配置", command=self.save_keys
        )
        self.button_save_key.pack(pady=(5, 10))

        # 刷新对象类型选择
        self.label_type = ctk.CTkLabel(self, text="刷新类型:")
        self.label_type.pack(pady=(10, 0))
        self.option_type = ctk.CTkOptionMenu(self, values=["File", "Directory"])
        self.option_type.pack(pady=5)

        # 刷新路径输入
        self.label_paths = ctk.CTkLabel(
            self, text="刷新路径（支持多行，每行一个URL或目录）:"
        )
        self.label_paths.pack(pady=(10, 0))
        self.text_paths = ctk.CTkTextbox(self, width=550, height=150)
        self.text_paths.pack(pady=5)

        # 加载路径历史
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                history = f.read().strip()
                self.text_paths.insert("1.0", history)

        # 刷新按钮
        self.button_refresh = ctk.CTkButton(
            self, text="执行刷新", command=self.refresh_cdn
        )
        self.button_refresh.pack(pady=20)

        self.progress = ctk.CTkProgressBar(self, width=550)
        self.progress.set(0)
        self.progress.pack(pady=(5, 20))

        # 输出结果
        self.label_output = ctk.CTkLabel(self, text="输出结果:")
        self.label_output.pack()
        self.text_output = ctk.CTkTextbox(self, width=550, height=200)
        self.text_output.pack(pady=5)

    def save_keys(self):
        ak_id = self.entry_id.get().strip()
        ak_secret = self.entry_secret.get().strip()
        if not ak_id or not ak_secret:
            messagebox.showerror("错误", "AccessKey ID 和 Secret 不能为空")
            return
        set_key(ENV_FILE, "ACCESS_KEY_ID", ak_id)
        set_key(ENV_FILE, "ACCESS_KEY_SECRET", ak_secret)
        messagebox.showinfo("成功", "AccessKey 已保存到 .env 文件")

    def refresh_cdn(self):
        thread = threading.Thread(target=self._refresh_cdn_and_track)
        thread.start()

    def _refresh_cdn_and_track(self):

        ak_id = self.entry_id.get().strip()
        ak_secret = self.entry_secret.get().strip()
        obj_type = self.option_type.get()
        obj_paths = self.text_paths.get("1.0", "end").strip()

        if not ak_id or not ak_secret or not obj_paths:
            # 保存 AccessKey 到 .env
            set_key(ENV_FILE, "ACCESS_KEY_ID", ak_id)
            set_key(ENV_FILE, "ACCESS_KEY_SECRET", ak_secret)

            # 保存路径历史
            with open(HISTORY_FILE, "w", encoding="utf-8") as f:
                f.write(obj_paths.strip())

            messagebox.showerror("错误", "请填写所有字段")
            return

        try:
            client = AcsClient(ak_id, ak_secret, "cn-hangzhou")
            refresh_req = RefreshObjectCachesRequest()
            refresh_req.set_accept_format("json")
            refresh_req.set_ObjectType(obj_type)
            refresh_req.set_ObjectPath(obj_paths)

            self.text_output.insert("end", f"发送刷新请求中...\n")
            result = client.do_action_with_exception(refresh_req)
            result_json = json.loads(result)
            task_id = result_json.get("RefreshTaskId")

            self.text_output.insert(
                "end", f"任务提交成功，任务ID：{task_id}\n正在等待任务完成...\n"
            )

            # 查询任务状态
            from aliyunsdkcdn.request.v20180510.DescribeRefreshTasksRequest import (
                DescribeRefreshTasksRequest,
            )
            import time

            while True:
                time.sleep(2)  # 每 2 秒查询一次
                query_req = DescribeRefreshTasksRequest()
                query_req.set_accept_format("json")
                query_req.set_TaskId(task_id)
                query_req.set_PageSize(1)

                query_resp = client.do_action_with_exception(query_req)
                query_data = json.loads(query_resp)
                task_info = query_data.get("Tasks", {}).get("CDNTask", [])[0]

                status = task_info.get("Status")
                process_str = task_info.get("Process", "0%").replace("%", "")
                try:
                    progress = int(process_str) / 100
                except:
                    progress = 0

                self.progress.set(progress)
                desc = f"当前状态: {status}, 进度: {process_str}%"
                self.text_output.insert("end", desc + "\n")
                self.text_output.see("end")

                if status in ["Complete", "Failed"]:
                    self.text_output.insert("end", f"任务已结束，状态：{status}\n")
                    break

        except Exception as e:
            self.text_output.insert("end", f"请求失败: {str(e)}\n")


if __name__ == "__main__":
    app = CDNRefreshApp()
    app.mainloop()
