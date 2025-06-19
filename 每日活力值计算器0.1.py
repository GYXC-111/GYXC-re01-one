import sys
import math
import json
import random
from datetime import datetime, timedelta
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton, QGroupBox, QMessageBox,
                             QTextEdit, QListWidget, QListWidgetItem, QComboBox, QCheckBox,
                             QSpinBox, QProgressBar, QStackedWidget, QDialog, QFormLayout)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont, QPalette, QColor, QIcon


class GoalSettingDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("设定新目标")
        self.setWindowIcon(QIcon(":icons/goal.png"))
        self.setGeometry(300, 300, 400, 300)
        self.setStyleSheet("""
            QDialog {
                background-color: #2c3e50;
                color: #ecf0f1;
            }
            QLabel {
                color: #bdc3c7;
            }
            QLineEdit, QComboBox, QSpinBox, QTextEdit {
                background-color: #34495e;
                border: 1px solid #7f8c8d;
                border-radius: 4px;
                padding: 5px;
                color: #ecf0f1;
            }
            QPushButton {
                background-color: #1abc9c;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #16a085;
            }
        """)

        layout = QVBoxLayout()

        form_layout = QFormLayout()

        self.goal_name = QLineEdit()
        self.goal_name.setPlaceholderText("例如：完成Python项目")
        form_layout.addRow("目标名称:", self.goal_name)

        self.goal_type = QComboBox()
        self.goal_type.addItems(["学习提升", "健康运动", "工作效率", "生活习惯", "个人兴趣"])
        form_layout.addRow("目标类型:", self.goal_type)

        self.duration = QSpinBox()
        self.duration.setRange(1, 365)
        self.duration.setValue(7)
        form_layout.addRow("持续时间(天):", self.duration)

        self.target_value = QSpinBox()
        self.target_value.setRange(1, 1000)
        self.target_value.setValue(100)
        form_layout.addRow("目标值:", self.target_value)

        self.unit = QComboBox()
        self.unit.addItems(["分钟", "小时", "页", "次", "公里", "千克"])
        form_layout.addRow("单位:", self.unit)

        self.description = QTextEdit()
        self.description.setPlaceholderText("描述目标细节和重要性...")
        form_layout.addRow("目标描述:", self.description)

        layout.addLayout(form_layout)

        button_layout = QHBoxLayout()
        save_btn = QPushButton("保存目标")
        save_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("取消")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def get_goal_data(self):
        return {
            "name": self.goal_name.text(),
            "type": self.goal_type.currentText(),
            "duration": self.duration.value(),
            "target": self.target_value.value(),
            "unit": self.unit.currentText(),
            "description": self.description.toPlainText(),
            "start_date": datetime.now().strftime("%Y-%m-%d"),
            "progress": 0,
            "completed": False
        }


class RewardSystemDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("设定奖励规则")
        self.setWindowIcon(QIcon(":icons/reward.png"))
        self.setGeometry(300, 300, 400, 300)
        self.setStyleSheet("""
            QDialog {
                background-color: #2c3e50;
                color: #ecf0f1;
            }
            QLabel {
                color: #bdc3c7;
            }
            QLineEdit, QSpinBox {
                background-color: #34495e;
                border: 1px solid #7f8c8d;
                border-radius: 4px;
                padding: 5px;
                color: #ecf0f1;
            }
            QPushButton {
                background-color: #1abc9c;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #16a085;
            }
        """)

        layout = QVBoxLayout()

        form_layout = QFormLayout()

        self.reward_name = QLineEdit()
        self.reward_name.setPlaceholderText("例如：看一场电影")
        form_layout.addRow("奖励名称:", self.reward_name)

        self.cost = QSpinBox()
        self.cost.setRange(1, 1000)
        self.cost.setValue(50)
        form_layout.addRow("所需活力值:", self.cost)

        self.reward_type = QComboBox()
        self.reward_type.addItems(["娱乐休闲", "美食享受", "购物消费", "自我提升", "社交活动"])
        form_layout.addRow("奖励类型:", self.reward_type)

        self.description = QLineEdit()
        self.description.setPlaceholderText("描述奖励内容...")
        form_layout.addRow("奖励描述:", self.description)

        layout.addLayout(form_layout)

        button_layout = QHBoxLayout()
        save_btn = QPushButton("保存规则")
        save_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("取消")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def get_reward_data(self):
        return {
            "name": self.reward_name.text(),
            "cost": self.cost.value(),
            "type": self.reward_type.currentText(),
            "description": self.description.text()
        }


class DisciplineSystem(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("自律成就系统")
        self.setWindowIcon(QIcon(":icons/discipline.png"))
        self.setGeometry(100, 100, 900, 700)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2c3e50;
                color: #ecf0f1;
            }
            QGroupBox {
                background-color: #34495e;
                border: 2px solid #3498db;
                border-radius: 10px;
                margin-top: 1ex;
                font-size: 14px;
                font-weight: bold;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
                color: #1abc9c;
            }
            QLabel {
                color: #bdc3c7;
                font-size: 13px;
            }
            QLineEdit, QComboBox, QSpinBox {
                background-color: #34495e;
                border: 1px solid #7f8c8d;
                border-radius: 4px;
                padding: 5px;
                color: #ecf0f1;
                font-size: 14px;
            }
            QPushButton {
                background-color: #1abc9c;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #16a085;
            }
            QPushButton:disabled {
                background-color: #7f8c8d;
            }
            QListWidget {
                background-color: #2c3e50;
                border: 1px solid #7f8c8d;
                border-radius: 5px;
                color: #ecf0f1;
                font-size: 13px;
            }
            QTextEdit {
                background-color: #2c3e50;
                border: 1px solid #7f8c8d;
                border-radius: 5px;
                color: #ecf0f1;
                font-size: 13px;
            }
            QProgressBar {
                border: 1px solid #34495e;
                border-radius: 7px;
                background-color: #2c3e50;
                text-align: center;
                font-size: 12px;
            }
            QProgressBar::chunk {
                background-color: #1abc9c;
                width: 10px;
            }
        """)

        # 初始化数据
        self.vitality = 100
        self.goals = []
        self.rewards = []
        self.history = []
        self.max_vitality = 100  # 记录最高活力值
        self.load_data()

        self.initUI()

    def load_data(self):
        try:
            with open("discipline_data.json", "r") as f:
                data = json.load(f)
                self.vitality = data.get("vitality", 100)
                self.max_vitality = data.get("max_vitality", self.vitality)
                self.goals = data.get("goals", [])
                self.rewards = data.get("rewards", [])
                self.history = data.get("history", [])
        except FileNotFoundError:
            # 初始化默认奖励
            self.rewards = [
                {"name": "30分钟娱乐时间", "cost": 30, "type": "娱乐休闲", "description": "自由安排娱乐活动"},
                {"name": "一杯精品咖啡", "cost": 20, "type": "美食享受", "description": "享受一杯高品质咖啡"},
                {"name": "购买一本书", "cost": 80, "type": "自我提升", "description": "购买一本感兴趣的书籍"},
                {"name": "周末电影", "cost": 60, "type": "娱乐休闲", "description": "周末看一场电影"},
                {"name": "美食大餐", "cost": 100, "type": "美食享受", "description": "享受一顿丰盛的美食"}
            ]

    def save_data(self):
        data = {
            "vitality": self.vitality,
            "max_vitality": self.max_vitality,
            "goals": self.goals,
            "rewards": self.rewards,
            "history": self.history
        }
        with open("discipline_data.json", "w") as f:
            json.dump(data, f, indent=2)

    def initUI(self):
        # 创建主部件和布局
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # 标题和活力值显示
        header_layout = QHBoxLayout()

        title = QLabel("自律成就系统")
        title.setFont(QFont("Arial", 24, QFont.Bold))
        title.setStyleSheet("color: #1abc9c;")

        vitality_box = QGroupBox("活力值")
        vitality_layout = QVBoxLayout()
        self.vitality_label = QLabel(f"{self.vitality} 点")
        self.vitality_label.setFont(QFont("Arial", 20, QFont.Bold))
        self.vitality_label.setAlignment(Qt.AlignCenter)
        self.vitality_label.setStyleSheet("color: #1abc9c;")
        vitality_layout.addWidget(self.vitality_label)
        vitality_box.setLayout(vitality_layout)

        header_layout.addWidget(title, 4)
        header_layout.addWidget(vitality_box, 1)

        # 核心规则说明
        rules = QLabel(
            "自律成就系统规则：\n"
            "1. 每日初始活力值 = 100点\n"
            "2. 完成目标可获得活力值奖励（目标价值的10-20%）\n"
            "3. 超额完成目标可获得额外奖励\n"
            "4. 未完成目标会扣除相应活力值（目标价值的5-10%）\n"
            "5. 活力值可用于兑换各种奖励\n"
            "6. 连续完成目标可获得成就徽章和额外奖励"
        )
        rules.setFont(QFont("Arial", 11))
        rules.setStyleSheet("background-color: #34495e; border-radius: 10px; padding: 10px;")

        # 创建堆叠窗口
        self.stacked_widget = QStackedWidget()

        # 目标管理页面
        goals_page = self.create_goals_page()
        self.stacked_widget.addWidget(goals_page)

        # 奖励系统页面
        rewards_page = self.create_rewards_page()
        self.stacked_widget.addWidget(rewards_page)

        # 历史记录页面
        history_page = self.create_history_page()
        self.stacked_widget.addWidget(history_page)

        # 导航按钮
        nav_layout = QHBoxLayout()
        goals_btn = QPushButton("目标管理")
        goals_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        rewards_btn = QPushButton("奖励系统")
        rewards_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        history_btn = QPushButton("成就历史")
        history_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))

        nav_layout.addWidget(goals_btn)
        nav_layout.addWidget(rewards_btn)
        nav_layout.addWidget(history_btn)

        # 添加到主布局
        main_layout.addLayout(header_layout)
        main_layout.addWidget(rules)
        main_layout.addLayout(nav_layout)
        main_layout.addWidget(self.stacked_widget, 1)

        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def create_goals_page(self):
        page = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(15)

        # 目标列表
        goals_group = QGroupBox("当前目标")
        goals_layout = QVBoxLayout()

        self.goals_list = QListWidget()
        self.goals_list.setMinimumHeight(200)
        self.goals_list.itemSelectionChanged.connect(self.goal_selected)
        self.update_goals_list()
        goals_layout.addWidget(self.goals_list)

        # 目标操作按钮
        goals_btn_layout = QHBoxLayout()
        add_goal_btn = QPushButton("添加目标")
        add_goal_btn.clicked.connect(self.add_goal)
        update_goal_btn = QPushButton("更新进度")
        update_goal_btn.clicked.connect(self.update_goal_progress)
        remove_goal_btn = QPushButton("移除目标")
        remove_goal_btn.clicked.connect(self.remove_goal)

        goals_btn_layout.addWidget(add_goal_btn)
        goals_btn_layout.addWidget(update_goal_btn)
        goals_btn_layout.addWidget(remove_goal_btn)

        goals_layout.addLayout(goals_btn_layout)
        goals_group.setLayout(goals_layout)

        # 目标进度区域
        progress_group = QGroupBox("目标进度")
        progress_layout = QVBoxLayout()

        form_layout = QFormLayout()

        self.goal_name_label = QLabel("未选择目标")
        form_layout.addRow("目标名称:", self.goal_name_label)

        self.progress_label = QLabel("0%")
        form_layout.addRow("当前进度:", self.progress_label)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        form_layout.addRow("进度条:", self.progress_bar)

        self.progress_input = QSpinBox()
        self.progress_input.setRange(0, 1000)
        self.progress_input.setValue(0)
        form_layout.addRow("新增进度:", self.progress_input)

        self.achieve_btn = QPushButton("记录进度")
        self.achieve_btn.clicked.connect(self.record_progress)
        self.achieve_btn.setEnabled(False)

        progress_layout.addLayout(form_layout)
        progress_layout.addWidget(self.achieve_btn)
        progress_group.setLayout(progress_layout)

        layout.addWidget(goals_group)
        layout.addWidget(progress_group)

        page.setLayout(layout)
        return page

    def create_rewards_page(self):
        page = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(15)

        # 奖励列表
        rewards_group = QGroupBox("奖励兑换")
        rewards_layout = QVBoxLayout()

        self.rewards_list = QListWidget()
        self.rewards_list.setMinimumHeight(200)
        self.update_rewards_list()
        rewards_layout.addWidget(self.rewards_list)

        # 奖励操作按钮
        rewards_btn_layout = QHBoxLayout()
        add_reward_btn = QPushButton("添加奖励")
        add_reward_btn.clicked.connect(self.add_reward)
        redeem_btn = QPushButton("兑换奖励")
        redeem_btn.clicked.connect(self.redeem_reward)
        remove_reward_btn = QPushButton("移除奖励")
        remove_reward_btn.clicked.connect(self.remove_reward)

        rewards_btn_layout.addWidget(add_reward_btn)
        rewards_btn_layout.addWidget(redeem_btn)
        rewards_btn_layout.addWidget(remove_reward_btn)

        rewards_layout.addLayout(rewards_btn_layout)
        rewards_group.setLayout(rewards_layout)

        # 兑换历史
        redeem_group = QGroupBox("兑换历史")
        redeem_layout = QVBoxLayout()

        self.redeem_history = QTextEdit()
        self.redeem_history.setReadOnly(True)
        self.update_redeem_history()

        redeem_layout.addWidget(self.redeem_history)
        redeem_group.setLayout(redeem_layout)

        layout.addWidget(rewards_group)
        layout.addWidget(redeem_group)

        page.setLayout(layout)
        return page

    def create_history_page(self):
        page = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(15)

        # 成就徽章
        badges_group = QGroupBox("成就徽章")
        badges_layout = QHBoxLayout()

        badges = [
            ("连续7天自律", "🏆", "#f1c40f", "连续7天完成所有目标"),
            ("目标大师", "🎯", "#9b59b6", "完成10个不同目标"),
            ("活力充沛", "💪", "#e74c3c", "单日活力值超过200点"),
            ("高效执行者", "⚡", "#2ecc71", "一周内完成5个目标")
        ]

        for name, icon, color, desc in badges:
            badge = QGroupBox()
            badge_layout = QVBoxLayout()

            badge_title = QLabel(f"{icon} {name}")
            badge_title.setFont(QFont("Arial", 12, QFont.Bold))
            badge_title.setStyleSheet(f"color: {color};")
            badge_title.setAlignment(Qt.AlignCenter)

            badge_desc = QLabel(desc)
            badge_desc.setAlignment(Qt.AlignCenter)
            badge_desc.setStyleSheet("font-size: 11px;")

            badge_layout.addWidget(badge_title)
            badge_layout.addWidget(badge_desc)
            badge.setLayout(badge_layout)
            badges_layout.addWidget(badge)

        badges_group.setLayout(badges_layout)

        # 历史记录
        history_group = QGroupBox("自律历史")
        history_layout = QVBoxLayout()

        self.history_display = QTextEdit()
        self.history_display.setReadOnly(True)
        self.update_history_display()

        history_layout.addWidget(self.history_display)
        history_group.setLayout(history_layout)

        # 统计信息
        stats_group = QGroupBox("统计信息")
        stats_layout = QVBoxLayout()

        stats_text = QLabel(
            f"总目标数: {len(self.goals)}\n"
            f"已完成目标: {sum(1 for g in self.goals if g['completed'])}\n"
            f"平均完成率: {self.calculate_average_completion()}%\n"
            f"最高单日活力值: {self.max_vitality}点\n"
            f"总兑换奖励: {sum(1 for h in self.history if h['type'] == 'redeem')}"
        )
        stats_text.setFont(QFont("Arial", 12))

        stats_layout.addWidget(stats_text)
        stats_group.setLayout(stats_layout)

        layout.addWidget(badges_group)
        layout.addWidget(history_group)
        layout.addWidget(stats_group)

        page.setLayout(layout)
        return page

    def update_goals_list(self):
        self.goals_list.clear()
        for goal in self.goals:
            progress_percent = int((goal['progress'] / goal['target']) * 100) if goal['target'] > 0 else 0
            status = "✓" if goal['completed'] else "◻"
            color = "#2ecc71" if goal['completed'] else ("#f39c12" if progress_percent > 0 else "#bdc3c7")

            item = QListWidgetItem(f"{status} [{goal['type']}] {goal['name']} - {progress_percent}%")
            item.setData(Qt.UserRole, goal)
            item.setForeground(QColor(color))
            self.goals_list.addItem(item)

        if self.goals_list.count() > 0:
            self.goals_list.setCurrentRow(0)
            self.goal_selected()

    def goal_selected(self):
        selected_items = self.goals_list.selectedItems()
        if not selected_items:
            self.goal_name_label.setText("未选择目标")
            self.progress_label.setText("0%")
            self.progress_bar.setValue(0)
            self.progress_input.setValue(0)
            self.achieve_btn.setEnabled(False)
            return

        goal = selected_items[0].data(Qt.UserRole)
        progress_percent = int((goal['progress'] / goal['target']) * 100) if goal['target'] > 0 else 0

        self.goal_name_label.setText(goal['name'])
        self.progress_label.setText(f"{goal['progress']}/{goal['target']} {goal['unit']} ({progress_percent}%)")
        self.progress_bar.setValue(min(100, progress_percent))
        self.progress_input.setValue(0)
        self.achieve_btn.setEnabled(not goal['completed'])

    def add_goal(self):
        dialog = GoalSettingDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            new_goal = dialog.get_goal_data()
            self.goals.append(new_goal)
            self.update_goals_list()
            self.save_data()

    def update_goal_progress(self):
        selected_items = self.goals_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "选择目标", "请先选择一个目标")
            return

        goal = selected_items[0].data(Qt.UserRole)
        self.goal_selected()

    def remove_goal(self):
        selected_items = self.goals_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "选择目标", "请先选择一个目标")
            return

        goal = selected_items[0].data(Qt.UserRole)
        reply = QMessageBox.question(self, "确认移除",
                                     f"确定要移除目标 '{goal['name']}' 吗?",
                                     QMessageBox.Yes | QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.goals = [g for g in self.goals if g != goal]
            self.update_goals_list()
            self.save_data()

    def record_progress(self):
        selected_items = self.goals_list.selectedItems()
        if not selected_items:
            return

        goal = selected_items[0].data(Qt.UserRole)
        progress = self.progress_input.value()

        if progress <= 0:
            QMessageBox.warning(self, "输入错误", "请输入有效的进度值")
            return

        # 更新目标进度
        goal['progress'] += progress

        # 检查目标是否完成
        completed = goal['progress'] >= goal['target']
        goal['completed'] = completed

        # 计算活力值变化
        progress_percent = (goal['progress'] / goal['target']) * 100
        reward = 0

        if completed:
            # 目标完成奖励
            base_reward = int(goal['target'] * 0.15)  # 目标价值的15%
            # 超额完成额外奖励
            if goal['progress'] > goal['target']:
                extra = goal['progress'] - goal['target']
                extra_reward = int(extra * 0.05)
                reward = base_reward + extra_reward
            else:
                reward = base_reward

            # 记录成就
            self.history.append({
                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "type": "achievement",
                "goal": goal['name'],
                "vitality_change": reward,
                "message": f"恭喜完成目标: {goal['name']}!"
            })
        else:
            # 部分完成奖励
            reward = int(progress * 0.10)  # 进度值的10%

            # 记录进度
            self.history.append({
                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "type": "progress",
                "goal": goal['name'],
                "vitality_change": reward,
                "message": f"为目标 '{goal['name']}' 添加了 {progress} {goal['unit']} 进度"
            })

        # 更新活力值
        self.vitality += reward

        # 更新最高活力值
        if self.vitality > self.max_vitality:
            self.max_vitality = self.vitality

        self.vitality_label.setText(f"{self.vitality} 点")

        # 更新UI
        self.update_goals_list()
        self.update_history_display()
        self.save_data()

        # 显示通知
        if completed:
            QMessageBox.information(self, "目标完成",
                                    f"恭喜完成目标 '{goal['name']}'!\n"
                                    f"获得活力值奖励: +{reward}点")
        else:
            QMessageBox.information(self, "进度更新",
                                    f"已为 '{goal['name']}' 添加 {progress} {goal['unit']} 进度\n"
                                    f"获得活力值奖励: +{reward}点")

    def update_rewards_list(self):
        self.rewards_list.clear()
        for reward in self.rewards:
            affordable = self.vitality >= reward['cost']
            color = "#2ecc71" if affordable else "#e74c3c"

            item = QListWidgetItem(f"[{reward['type']}] {reward['name']} - {reward['cost']}点")
            item.setData(Qt.UserRole, reward)
            item.setForeground(QColor(color))
            self.rewards_list.addItem(item)

    def add_reward(self):
        dialog = RewardSystemDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            new_reward = dialog.get_reward_data()
            self.rewards.append(new_reward)
            self.update_rewards_list()
            self.save_data()

    def redeem_reward(self):
        selected_items = self.rewards_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "选择奖励", "请先选择一个奖励")
            return

        reward = selected_items[0].data(Qt.UserRole)

        if self.vitality < reward['cost']:
            QMessageBox.warning(self, "活力值不足",
                                f"兑换 '{reward['name']}' 需要 {reward['cost']}点活力值\n"
                                f"当前活力值: {self.vitality}点")
            return

        # 确认兑换
        reply = QMessageBox.question(self, "确认兑换",
                                     f"确定要兑换 '{reward['name']}'?\n"
                                     f"将消耗 {reward['cost']}点活力值",
                                     QMessageBox.Yes | QMessageBox.No)

        if reply == QDialog.Accepted:
            # 更新活力值
            self.vitality -= reward['cost']
            self.vitality_label.setText(f"{self.vitality} 点")

            # 记录历史
            self.history.append({
                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "type": "redeem",
                "reward": reward['name'],
                "vitality_change": -reward['cost'],
                "message": f"兑换奖励: {reward['name']}"
            })

            # 更新UI
            self.update_rewards_list()
            self.update_redeem_history()
            self.update_history_display()
            self.save_data()

            # 显示兑换成功消息
            QMessageBox.information(self, "兑换成功",
                                    f"已成功兑换 '{reward['name']}'\n"
                                    f"消耗活力值: {reward['cost']}点\n"
                                    f"剩余活力值: {self.vitality}点")

    def remove_reward(self):
        selected_items = self.rewards_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "选择奖励", "请先选择一个奖励")
            return

        reward = selected_items[0].data(Qt.UserRole)
        reply = QMessageBox.question(self, "确认移除",
                                     f"确定要移除奖励 '{reward['name']}' 吗?",
                                     QMessageBox.Yes | QMessageBox.No)

        if reply == QDialog.Accepted:
            self.rewards = [r for r in self.rewards if r != reward]
            self.update_rewards_list()
            self.save_data()

    def update_redeem_history(self):
        """更新兑换历史显示"""
        redeem_history = "兑换历史:\n"
        redeem_history += "=" * 40 + "\n"

        # 筛选兑换类型的记录
        redeem_entries = [h for h in self.history if h['type'] == 'redeem']

        # 只显示最近的10条记录
        for entry in redeem_entries[-10:]:
            redeem_history += f"{entry['date']} - {entry['reward']} (-{abs(entry['vitality_change'])}点)\n"

        self.redeem_history.setText(redeem_history)

    def update_history_display(self):
        """更新成就历史显示"""
        history_text = "自律成就历史:\n"
        history_text += "=" * 60 + "\n"

        # 只显示最近的15条记录
        for entry in self.history[-15:]:
            change = entry['vitality_change']
            sign = "+" if change >= 0 else ""

            # 根据记录类型添加不同的图标
            if entry['type'] == 'achievement':
                history_text += f"🏆 {entry['date']} - {entry['message']} ({sign}{change}点)\n"
            elif entry['type'] == 'progress':
                history_text += f"📈 {entry['date']} - {entry['message']} ({sign}{change}点)\n"
            elif entry['type'] == 'redeem':
                history_text += f"🎁 {entry['date']} - {entry['message']} ({sign}{change}点)\n"

        self.history_display.setText(history_text)

    def calculate_average_completion(self):
        if not self.goals:
            return 0

        total_percent = 0
        for goal in self.goals:
            progress_percent = min(100, (goal['progress'] / goal['target']) * 100) if goal['target'] > 0 else 0
            total_percent += progress_percent

        return round(total_percent / len(self.goals), 1)

    def closeEvent(self, event):
        self.save_data()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # 设置应用样式
    app.setStyle("Fusion")

    # 创建图标
    app.setWindowIcon(QIcon(":icons/discipline.png"))

    # 创建主窗口
    window = DisciplineSystem()
    window.show()

    sys.exit(app.exec_())