import sys
import vtk
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import Qt
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor


class MainWindow(Qt.QMainWindow):

    def __init__(self, parent=None):
        Qt.QMainWindow.__init__(self, parent)
        
        self.setWindowTitle("COSC 6344 Visualization final project: Ray Casting With GPU support and SemiAuto Tranfer function")
        self.resize(1000, self.height())
        self.frame = Qt.QFrame()
        self.mainLayout = Qt.QHBoxLayout()
        self.frame.setLayout(self.mainLayout)
        self.setCentralWidget(self.frame)
        
        self.vtkWidget = QVTKRenderWindowInteractor(self.frame)
        self.mainLayout.addWidget(self.vtkWidget)
        
        self.init_vtk_widget()
        
        self.right_panel_widget = Qt.QWidget()
        self.right_panel_layout = Qt.QVBoxLayout()
        self.right_panel_widget.setLayout(self.right_panel_layout)
        self.mainLayout.addWidget(self.right_panel_widget)
        
        self.volumeColor = vtk.vtkColorTransferFunction()
        self.volumeScalarOpacity = vtk.vtkPiecewiseFunction()
        self.volume = vtk.vtkVolume()
        self.volume_Opacity = []
        self.volume_Gradient = []
        
        
        
        #default scalar value
        self.scalar_value_to_update = 500
        
        self.add_controls()

    def init_vtk_widget(self):
        vtk.vtkObject.GlobalWarningDisplayOff()
        self.ren = vtk.vtkRenderer()
        self.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()
        colors = vtk.vtkNamedColors()
        self.ren.SetBackground(0.8, 0.8, 0.8)

        self.bwLut = vtk.vtkLookupTable()
        self.bwLut.SetTableRange(0, 2)
        self.bwLut.SetSaturationRange(0, 0)
        self.bwLut.SetHueRange(0, 0)
        self.bwLut.SetValueRange(0, 1)
        self.bwLut.Build()

        self.ren.ResetCamera()
        self.show()
        self.iren.Initialize()
        self.iren.Start()

    def show_popup_message(self, msg):
        alert = Qt.QMessageBox()
        alert.setText(msg)
        alert.exec_()

    def add_controls(self):
        groupBox = Qt.QGroupBox("Ray Casting With GPU support and SemiAuto Tranfer function")
        groupBox_layout = Qt.QVBoxLayout()
        groupBox.setLayout(groupBox_layout)
        self.right_panel_layout.addWidget(groupBox)

        label = Qt.QLabel("Choose a Data file:")
        groupBox_layout.addWidget(label)
        hbox = Qt.QHBoxLayout()
        self.ui_file_name = Qt.QLineEdit()
        hbox.addWidget(self.ui_file_name)
        self.ui_browser_button = Qt.QPushButton('Browser')
        self.ui_browser_button.clicked.connect(self.on_file_browser_clicked)
        self.ui_browser_button.show()
        hbox.addWidget(self.ui_browser_button)
        file_widget = Qt.QWidget()
        file_widget.setLayout(hbox)
        groupBox_layout.addWidget(file_widget)

        self.ui_open_button = Qt.QPushButton('Open')
        self.ui_open_button.clicked.connect(self.open_vtk_file)
        self.ui_open_button.show()
        groupBox_layout.addWidget(self.ui_open_button)

        self.ui_min_label = Qt.QLabel("Min Scalar: 0")
        self.ui_max_label = Qt.QLabel("Max Scalar: 0")
        groupBox_layout.addWidget(self.ui_min_label)
        groupBox_layout.addWidget(self.ui_max_label)



        groupBox_layout.addWidget(Qt.QLabel("Raycasting:"))

        hbox = Qt.QHBoxLayout()
        self.ui_dvr_checkbox = Qt.QCheckBox("Show Volume Rendering: ")
        self.ui_dvr_checkbox.setChecked(False)
        self.ui_dvr_checkbox.toggled.connect(self.on_checkbox_change)
        hbox.addWidget(self.ui_dvr_checkbox)
        ui_volWidget = Qt.QWidget()
        ui_volWidget.setLayout(hbox)

        '''
        self.ui_lcp_button = Qt.QPushButton('Load Control Points')
        self.ui_lcp_button.clicked.connect(self.load_color_transfer_values)
        self.ui_lcp_button.show()
        hbox.addWidget(self.ui_lcp_button)
        '''

        groupBox_layout.addWidget(ui_volWidget)

        ''' Add controls for interactive transfer function '''
        groupBox_layout.addWidget(Qt.QLabel("Interactive Transfer Function:"))
        
        self.ui_update_scalar_button = Qt.QPushButton('Update Scalar Value', self)
        self.ui_update_scalar_button.clicked.connect(self.update_scalar_value)
        groupBox_layout.addWidget(self.ui_update_scalar_button)
        
        
        self.opacity_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.opacity_slider = Qt.QSlider(Qt.Qt.Horizontal)
        self.opacity_slider.setMinimum(0)
        self.opacity_slider.setMaximum(3500)
        self.opacity_slider.setTickPosition(Qt.QSlider.TicksBelow)
        self.opacity_slider.setTickInterval(10)
        self.opacity_slider.valueChanged.connect(self.change_opacity)
        
        groupBox_layout.addWidget(QtWidgets.QLabel("Opacity:"))
        groupBox_layout.addWidget(self.opacity_slider)
        
        self.gradinat_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.gradinat_slider = Qt.QSlider(Qt.Qt.Horizontal)
        self.gradinat_slider.setMinimum(0)
        self.gradinat_slider.setMaximum(3500)
        self.gradinat_slider.setTickPosition(Qt.QSlider.TicksBelow)
        self.gradinat_slider.setTickInterval(10)
        self.gradinat_slider.valueChanged.connect(self.change_gradiant)
        
        groupBox_layout.addWidget(QtWidgets.QLabel("Gradiant:"))
        groupBox_layout.addWidget(self.gradinat_slider)
        
        
        

        #layout = QtWidgets.QVBoxLayout(self)
    
        self.color_sliders = [QtWidgets.QSlider(QtCore.Qt.Horizontal) for _ in range(3)]
        color_layout = QtWidgets.QHBoxLayout()
        color_layout.addWidget(QtWidgets.QLabel("Red:"))
        color_layout.addWidget(self.color_sliders[0])
        color_layout.addWidget(QtWidgets.QLabel("Green:"))
        color_layout.addWidget(self.color_sliders[1])
        color_layout.addWidget(QtWidgets.QLabel("Blue:"))
        color_layout.addWidget(self.color_sliders[2])
        groupBox_layout.addLayout(color_layout)
        

        

        for slider in self.color_sliders:
            slider.valueChanged.connect(self.update_transfer_function)
        



    def on_file_browser_clicked(self):
        dlg = Qt.QFileDialog()
        dlg.setFileMode(Qt.QFileDialog.AnyFile)
        dlg.setNameFilter("loadable files (*.mhd)")

        if dlg.exec_():
            filenames = dlg.selectedFiles()
            self.ui_file_name.setText(filenames[0])

    def open_vtk_file(self):
        input_file_name = self.ui_file_name.text()

        if ".mhd" in input_file_name:
            self.input_type = "mhd"
            self.reader = vtk.vtkMetaImageReader()
            self.reader.SetFileName(input_file_name)
            self.reader.Update()
        elif ".vtk" in input_file_name:
            self.input_type = "vtk"
            self.reader = vtk.vtkDataSetReader()
            self.reader.SetFileName(input_file_name)
            self.reader.Update()
            self.reader.GetOutput().GetPointData().SetActiveScalars('s')
        elif ".raw" in input_file_name:
            self.input_type = "mha"
            self.reader = vtk.vtkMetaImageReader()
            self.reader.SetFileName(input_file_name)
            self.reader.Update()


        self.scalar_range = [self.reader.GetOutput().GetScalarRange()[0], self.reader.GetOutput().GetScalarRange()[1]]
        self.ui_min_label.setText("Min Scalar:" + str(self.scalar_range[0]))
        self.ui_max_label.setText("Max Scalar:" + str(self.scalar_range[1]))


        self.dim = self.reader.GetOutput().GetDimensions()


        outlineData = vtk.vtkOutlineFilter()
        outlineData.SetInputConnection(self.reader.GetOutputPort())
        outlineData.Update()

        mapOutline = vtk.vtkPolyDataMapper()
        mapOutline.SetInputConnection(outlineData.GetOutputPort())

        self.outline = vtk.vtkActor()
        self.outline.SetMapper(mapOutline)
        colors = vtk.vtkNamedColors()
        self.outline.GetProperty().SetColor(colors.GetColor3d("Black"))
        self.outline.GetProperty().SetLineWidth(2.)

        self.ren.AddActor(self.outline)
        self.ren.ResetCamera()
        self.vtkWidget.GetRenderWindow().Render()
        
        
    
        
    def update_transfer_function(self):
        # Update color transfer function
        for i, slider in enumerate(self.color_sliders):
            self.volumeColor.AddRGBPoint(
                slider.value(), 
                self.color_sliders[0].value() / 100.0,
                self.color_sliders[1].value() / 100.0,
                self.color_sliders[2].value() / 100.0
            )
            
        # Update opacity transfer function
        self.volumeScalarOpacity.RemoveAllPoints()
        self.volumeScalarOpacity.AddPoint(self.opacity_slider.value(), 0.0)
        self.volumeScalarOpacity.AddPoint(5000, 1.0)
        
        # Update Gradiant transfer function
        self.volumeGradientOpacity.RemoveAllPoints()
        self.volumeGradientOpacity.AddPoint(self.gradinat_slider.value(), 0.0)
        self.volumeGradientOpacity.AddPoint(5000, 1.0)
    
        # Apply the transfer functions to the volume property
        volume_property = vtk.vtkVolumeProperty()
        volume_property.SetColor(self.volumeColor)
        volume_property.SetScalarOpacity(self.volumeScalarOpacity)
        volume_property.SetInterpolationTypeToLinear()
    
        self.volume.SetProperty(volume_property)
    
        # Render the updated scene
        self.vtkWidget.GetRenderWindow().Render()


        
    def change_opacity(self, value):
        opacity_percentage = value
        #self.label_opacity_slider.setText(f"Opacity: {opacity_percentage}%")
        

        new_opacity_value = opacity_percentage / 100.0

        # Find and update the corresponding opacity value in self.volume_opacity
        for i, entry in enumerate(self.volume_Opacity):
            if entry[0] == self.scalar_value_to_update:
                self.vvolumeScalarOpacity[i][1] = new_opacity_value
                break

        # Call the function to update the visualization based on the new transfer function
        self.update_transfer_function()
        
        
    def change_gradiant(self, value):
        gradiant_percentage = value
        #self.label_opacity_slider.setText(f"Opacity: {opacity_percentage}%")
        

        new_gradiant_value = gradiant_percentage / 100.0

        # Find and update the corresponding opacity value in self.volume_opacity
        for i, entry in enumerate(self.volume_Gradient):
            if entry[0] == self.scalar_value_to_update:
                self.volumeGradientOpacity[i][1] = new_gradiant_value
                break

        # Call the function to update the visualization based on the new transfer function
        self.update_transfer_function()


            
            
    def update_scalar_value(self):
        # Prompt the user for a new scalar value
        self.scalar_value_to_update, ok_pressed = Qt.QInputDialog.getInt(
            self, "Scalar Value", "Enter Scalar Value to Update", 500, 0, 10000, 1
        )

        if not ok_pressed:
            return  # User canceled the input dialog

        # Now you can use scalar_value_to_update as needed in your code
        print(f"Scalar value to update: {self.scalar_value_to_update}")
        # Add your logic to update the scalar value as needed
        # For example, you can call self.change_opacity(scalar_value_to_update)

        # Update the visualization based on the new scalar value
        self.update_transfer_function()




    def comp_raycasting(self):
        
        # The volume will be displayed by ray-cast alpha compositing.
        # A ray-cast mapper is needed to do the ray-casting.
        self.volumeMapper = vtk.vtkGPUVolumeRayCastMapper()
        self.volumeMapper.SetInputConnection(self.reader.GetOutputPort())
    
       
      
            
        #Initial Control Points for colors
    
        self.volumeColor.AddRGBPoint(0, 0.0, 0.0, 0.0)
        self.volumeColor.AddRGBPoint(500, 1.0, 0.5, 0.3)
        self.volumeColor.AddRGBPoint(750, 0.0, 1.0, 0.0)  # Additional control point
        self.volumeColor.AddRGBPoint(1000, 1.0, 0.5, 0.3)
        self.volumeColor.AddRGBPoint(1250, 0.0, 0.0, 1.0)  # Additional control point
        self.volumeColor.AddRGBPoint(1500, 1.0, 1.0, 0.9)
    
        
        #Initial Control Points for opacity
        #self.volumeScalarOpacity.AddPoint(0, 0.0)
        #self.volumeScalarOpacity.AddPoint(90, 0.5)
        #self.volumeScalarOpacity.AddPoint(100, 1.0)
    
        # Use gradient information to enhance DVR
        
        self.volumeGradientOpacity = vtk.vtkPiecewiseFunction()
        self.volumeGradientOpacity.AddPoint(0, 0.0)
        self.volumeGradientOpacity.AddPoint(90, 0.5)
        self.volumeGradientOpacity.AddPoint(100, 1.0)
    
        # Next, you should set the volume property
        self.volumeProperty = vtk.vtkVolumeProperty()
        self.volumeProperty.SetColor(self.volumeColor)
        self.volumeProperty.SetScalarOpacity(self.volumeScalarOpacity)
        self.volumeProperty.SetGradientOpacity(self.volumeGradientOpacity)  # Set gradient opacity
        self.volumeProperty.SetInterpolationTypeToLinear()
    
        self.volumeProperty.ShadeOn()
        self.volumeProperty.SetAmbient(0.4)
        self.volumeProperty.SetDiffuse(0.6)
        self.volumeProperty.SetSpecular(0.2)
    
        # Create a vtkVolume object
        # set its mapper created above and its property.
        #self.volume = vtk.vtkVolume()
        self.volume.SetMapper(self.volumeMapper)
        self.volume.SetProperty(self.volumeProperty)
    
        # Finally, add the volume to the renderer
        self.ren.AddViewProp(self.volume)
        self.vtkWidget.GetRenderWindow().Render()
        
        

         
    def on_checkbox_change(self):
        if self.ui_dvr_checkbox.isChecked() == False:
            if hasattr(self, 'volume'):
                self.ren.RemoveViewProp(self.volume)
            self.vtkWidget.GetRenderWindow().Render()
        else:
            
            self.comp_raycasting()
            self.vtkWidget.GetRenderWindow().Render()
            
            

if __name__ == "__main__":
    app = Qt.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
