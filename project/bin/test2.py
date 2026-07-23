import sys
import time
import threading
import cv2
import dlib
import numpy as np
from pathlib import Path
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel, 
                            QVBoxLayout, QHBoxLayout, QWidget, QFileDialog,
                            QProgressBar, QMessageBox, QSplitter, QFrame)
from PyQt5.QtGui import QPixmap, QImage, QFont
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QUrl

# 设置路径
sys.path[0] = str(Path(sys.path[0]).parent)
from lib.MorphabelModel import TraditionalMorphableModel as Model
from lib.Renderer import Renderer

# 全局变量和模型初始化
DETECTOR = dlib.get_frontal_face_detector()
PREDICTOR = dlib.shape_predictor("F:/KKU IS REASEARCH/project/model/shape_predictor_68_face_landmarks.dat")
STD_SIZE = 120

class ProcessingThread(QThread):
    """处理线程，用于在后台处理图片，避免UI卡顿"""
    update_progress = pyqtSignal(int)
    processing_complete = pyqtSignal(object, object)
    processing_error = pyqtSignal(str)
    
    def __init__(self, image_path, model):
        super().__init__()
        self.image_path = image_path
        self.model = model
        self.running = True
        
    def run(self):
        try:
            # 读取图片
            self.update_progress.emit(10)
            frame = cv2.imread(self.image_path)
            if frame is None:
                self.processing_error.emit("无法读取图片，请检查文件是否有效")
                return
                
            frame = cv2.resize(frame, None, fx=2, fy=2)
            self.update_progress.emit(20)
            
            # 检测人脸
            faces = DETECTOR(frame, 1)
            if not len(faces):
                self.processing_error.emit("未检测到人脸，请选择包含人脸的图片")
                return
                
            self.update_progress.emit(30)
            
            # 处理帧
            clip, clipKeyPoints, keyPoints = self.processFrame(frame, faces[0])
            frame, keyPoints = clip, clipKeyPoints
            self.update_progress.emit(40)
            
            # 模型拟合
            start_time = time.time()
            self.model.fit(clip, clipKeyPoints)
            end_time = time.time()
            print(f'模型拟合耗时: {end_time - start_time:.4f}秒')
            self.update_progress.emit(70)
            
            # 绘制关键点
            for i in range(keyPoints.shape[1]):
                cv2.circle(frame, (keyPoints[0, i], keyPoints[1, i]), 1, (255, 0, 0), -1)
            
            # 准备渲染
            vertices, colors = self.model.transform()
            colors[:] = 1
            indices = self.model.tri.flatten()
            
            scale = 2.5 / np.max(np.max(vertices, axis=0) - np.min(vertices, axis=0))
            vertices *= scale
            colors[self.model.kptInd[:]] = [0, 0, 1]
            
            self.update_progress.emit(90)
            
            # 返回处理结果
            self.processing_complete.emit(frame, (vertices, colors, indices))
            
        except Exception as e:
            self.processing_error.emit(f"处理出错: {str(e)}")
    
    def processFrame(self, frame, face):
        """处理帧，提取人脸和关键点"""
        shape = PREDICTOR(frame, face)
        keyPoints = np.array([[p.x, p.y] for p in shape.parts()]).T
        
        detail = dlib.get_face_chip_details(shape, size=STD_SIZE, padding=0.5)
        clip = dlib.extract_image_chip(frame, detail)
        
        clipFace = DETECTOR(clip, 1)[0]
        clipShape = PREDICTOR(clip, clipFace)
        clipKeyPoints = np.array([[p.x, p.y] for p in clipShape.parts()]).T
        
        return clip, clipKeyPoints, keyPoints
        
    def stop(self):
        self.running = False
        self.wait()

class FaceMorphingApp(QMainWindow):
    """人脸建模与渲染应用主窗口"""
    def __init__(self):
        super().__init__()
        self.initUI()
        self.initModel()
        self.processing_thread = None
        
    def initUI(self):
        """初始化用户界面（优化版）"""
        # 基础配置
        self.setWindowTitle('人脸3D建模与渲染')
        self.setGeometry(100, 100, 1200, 800)  # 增大初始窗口尺寸
        self.setFont(QFont("SimHei", 9))  # 确保中文显示正常

        # 主布局（垂直）
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(15, 15, 15, 15)  # 外间距
        main_layout.setSpacing(12)  # 控件间距

        # 1. 顶部控制区域
        control_frame = QFrame()
        control_frame.setFrameShape(QFrame.StyledPanel)
        control_frame.setStyleSheet("background-color: #f5f5f5; border-radius: 4px;")
        control_layout = QHBoxLayout(control_frame)
        control_layout.setContentsMargins(10, 10, 10, 10)
        control_layout.setSpacing(15)

        # 选择图片按钮
        self.select_btn = QPushButton('📂 选择图片')
        self.select_btn.setMinimumHeight(32)
        self.select_btn.setStyleSheet("""
            QPushButton {
                background-color: #4285f4;
                color: white;
                border-radius: 4px;
                padding: 0 15px;
            }
            QPushButton:hover {
                background-color: #3367d6;
            }
        """)
        self.select_btn.clicked.connect(self.selectImage)
        control_layout.addWidget(self.select_btn)

        # 处理按钮
        self.process_btn = QPushButton('▶️ 开始处理')
        self.process_btn.setMinimumHeight(32)
        self.process_btn.setStyleSheet("""
            QPushButton {
                background-color: #34a853;
                color: white;
                border-radius: 4px;
                padding: 0 15px;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
            QPushButton:hover:enabled {
                background-color: #2a8644;
            }
        """)
        self.process_btn.clicked.connect(self.startProcessing)
        self.process_btn.setEnabled(False)
        control_layout.addWidget(self.process_btn)

        # 进度条（占剩余空间）
        control_layout.addStretch(1)  # 拉伸因子，让进度条占据更多空间
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimumHeight(32)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #ddd;
                border-radius: 4px;
                text-align: center;
                background-color: white;
            }
            QProgressBar::chunk {
                background-color: #4285f4;
                border-radius: 3px;
            }
        """)
        control_layout.addWidget(self.progress_bar, 3)  # 进度条占3份空间

        main_layout.addWidget(control_frame)

        # 2. 中间预览区域（可调整比例的分割器）
        preview_splitter = QSplitter(Qt.Horizontal)
        preview_splitter.setHandleWidth(6)  # 分割线宽度
        preview_splitter.setStyleSheet("QSplitter::handle { background-color: #ddd; border-radius: 3px; }")

        # 原始图片预览面板
        original_frame = QFrame()
        original_frame.setFrameShape(QFrame.StyledPanel)
        original_frame.setStyleSheet("border: 1px solid #ddd; border-radius: 4px;")
        original_vbox = QVBoxLayout(original_frame)
        original_vbox.setContentsMargins(10, 10, 10, 10)
        
        self.original_title = QLabel('原始图片')
        self.original_title.setAlignment(Qt.AlignLeft)
        self.original_title.setStyleSheet("font-weight: bold; color: #333; margin-bottom: 5px;")
        original_vbox.addWidget(self.original_title)
        
        self.original_label = QLabel('请选择图片')
        self.original_label.setAlignment(Qt.AlignCenter)
        self.original_label.setMinimumSize(400, 400)
        self.original_label.setStyleSheet("""
            border: 1px dashed #bbb; 
            border-radius: 3px; 
            color: #999;
            background-color: #fafafa;
        """)
        original_vbox.addWidget(self.original_label, 1)  # 图片区域占主要空间
        preview_splitter.addWidget(original_frame)

        # 处理结果预览面板
        result_frame = QFrame()
        result_frame.setFrameShape(QFrame.StyledPanel)
        result_frame.setStyleSheet("border: 1px solid #ddd; border-radius: 4px;")
        result_vbox = QVBoxLayout(result_frame)
        result_vbox.setContentsMargins(10, 10, 10, 10)
        
        self.result_title = QLabel('处理结果（带关键点）')
        self.result_title.setAlignment(Qt.AlignLeft)
        self.result_title.setStyleSheet("font-weight: bold; color: #333; margin-bottom: 5px;")
        result_vbox.addWidget(self.result_title)
        
        self.result_label = QLabel('等待处理...')
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setMinimumSize(400, 400)
        self.result_label.setStyleSheet("""
            border: 1px dashed #bbb; 
            border-radius: 3px; 
            color: #999;
            background-color: #fafafa;
        """)
        result_vbox.addWidget(self.result_label, 1)
        preview_splitter.addWidget(result_frame)

        # 设置初始分割比例（1:1）
        preview_splitter.setSizes([600, 600])
        main_layout.addWidget(preview_splitter, 3)  # 预览区占3份空间（最重要）

        # 3. 底部状态区域
        status_frame = QFrame()
        status_frame.setFrameShape(QFrame.StyledPanel)
        status_frame.setStyleSheet("background-color: #f9f9f9; border-radius: 4px;")
        status_layout = QHBoxLayout(status_frame)
        status_layout.setContentsMargins(10, 8, 10, 8)

        self.status_label = QLabel('请选择一张包含人脸的图片进行处理')
        self.status_label.setStyleSheet("color: #555;")
        status_layout.addWidget(self.status_label)
        
        # 增加额外信息标签（显示文件名）
        self.file_info_label = QLabel('')
        self.file_info_label.setStyleSheet("color: #777;")
        self.file_info_label.setAlignment(Qt.AlignRight)
        status_layout.addWidget(self.file_info_label)

        main_layout.addWidget(status_frame)

        # 设置中心部件
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # 初始化渲染器
        self.renderer = Renderer()
        
    def initModel(self):
        """初始化模型"""
        try:
            self.morphable_model = Model(
                filePath=r'F:\KKU IS REASEARCH\project\model\BFM.mat',
                maxIter=3,
                modelPath=r'F:\KKU IS REASEARCH\project\model/fit_model.pth',
                labelPath=r'F:\KKU IS REASEARCH\project\data\300W_LP\LFPW\LFPW_image_train_0645_1.mat'
            )
            self.status_label.setText("模型初始化成功，等待图片选择...")
        except Exception as e:
            self.status_label.setText(f"模型初始化失败: {str(e)}")
            QMessageBox.critical(self, "初始化错误", f"无法加载模型: {str(e)}")
    
    def selectImage(self):
        """选择图片文件"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择图片", "", "图片文件 (*.png *.jpg *.jpeg *.bmp)"
        )
        
        if file_path:
            self.image_path = file_path
            self.displayOriginalImage(file_path)
            self.process_btn.setEnabled(True)
            self.status_label.setText("已选择图片，点击「开始处理」生成3D模型")
            self.file_info_label.setText(f"文件: {Path(file_path).name}")
    
    def displayOriginalImage(self, file_path):
        """显示原始图片（优化缩放逻辑）"""
        pixmap = QPixmap(file_path)
        if not pixmap.isNull():
            # 按标签尺寸等比例缩放，最大边长不超过标签尺寸
            scaled_pixmap = pixmap.scaled(
                self.original_label.size(), 
                Qt.KeepAspectRatio, 
                Qt.SmoothTransformation
            )
            self.original_label.setPixmap(scaled_pixmap)
            self.original_label.setText('')  # 清空提示文字
    
    def startProcessing(self):
        """开始处理图片"""
        if not hasattr(self, 'image_path'):
            QMessageBox.warning(self, "警告", "请先选择一张图片")
            return
            
        self.process_btn.setEnabled(False)
        self.select_btn.setEnabled(False)
        self.progress_bar.setValue(0)
        self.status_label.setText("正在处理图片...（检测人脸→提取特征→模型拟合→渲染准备）")
        self.result_label.setText("处理中，请稍候...")
        
        # 创建并启动处理线程
        self.processing_thread = ProcessingThread(self.image_path, self.morphable_model)
        self.processing_thread.update_progress.connect(self.updateProgress)
        self.processing_thread.processing_complete.connect(self.onProcessingComplete)
        self.processing_thread.processing_error.connect(self.onProcessingError)
        self.processing_thread.start()
    
    def updateProgress(self, value):
        """更新进度条"""
        self.progress_bar.setValue(value)
    
    def onProcessingComplete(self, processed_frame, render_data):
        """处理完成时的回调"""
        self.progress_bar.setValue(100)
        
        # 显示处理后的图片（带关键点）
        self.displayProcessedImage(processed_frame)
        
        # 渲染3D模型
        vertices, colors, indices = render_data
        self.renderer.setModel(vertices, colors, indices)
        self.renderer.setCompare(np.ascontiguousarray(processed_frame[:,::-1,::-1]))
        
        # 更新状态，提示用户交互方式
        self.status_label.setText("处理完成！3D模型已生成，可通过鼠标交互进行旋转/缩放操作")
        self.process_btn.setEnabled(True)
        self.select_btn.setEnabled(True)
        
        # 显示渲染窗口（移除对setWindowTitle的调用，因为Renderer不是Qt窗口）
        self.renderer.show()
    
    def onProcessingError(self, error_msg):
        """处理错误时的回调"""
        self.status_label.setText(f"处理失败：{error_msg}")
        self.result_label.setText("处理失败，请重新尝试")
        QMessageBox.error(self, "处理错误", error_msg)
        self.process_btn.setEnabled(True)
        self.select_btn.setEnabled(True)
    
    def displayProcessedImage(self, frame):
        """显示处理后的图片（优化显示逻辑）"""
        # 转换OpenCV图像格式为Qt可显示的格式
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        q_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        
        # 缩放图片以适应标签
        scaled_image = q_image.scaled(
            self.result_label.size(), 
            Qt.KeepAspectRatio, 
            Qt.SmoothTransformation
        )
        self.result_label.setPixmap(QPixmap.fromImage(scaled_image))
        self.result_label.setText('')  # 清空提示文字
    
    def resizeEvent(self, event):
        """窗口大小改变时，重新调整图片显示"""
        if hasattr(self, 'image_path'):
            self.displayOriginalImage(self.image_path)
        super().resizeEvent(event)
    
    def closeEvent(self, event):
        """窗口关闭时的处理"""
        if self.processing_thread and self.processing_thread.isRunning():
            self.processing_thread.stop()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FaceMorphingApp()
    window.show()
    sys.exit(app.exec_())
