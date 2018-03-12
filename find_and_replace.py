import os
from hutil.Qt import QtCore
from hutil.Qt import QtWidgets

class findAndReplace(QtWidgets.QWidget):
    def __init__(self, parent=None):
    
        # INITIALIZE GUI AND SET WINDOW TO ALWAYS ON TOP
        QtWidgets.QWidget.__init__(self, parent, QtCore.Qt.WindowStaysOnTopHint)

        # SET LAYOUTS
        vbox = QtWidgets.QVBoxLayout()
        hbox1 = QtWidgets.QHBoxLayout()
        hbox2 = QtWidgets.QHBoxLayout()
        hbox3 = QtWidgets.QHBoxLayout()
        hbox4 = QtWidgets.QHBoxLayout()
        hbox_checkboxes1 = QtWidgets.QHBoxLayout()
        hbox_checkboxes2 = QtWidgets.QHBoxLayout()        
        hbox_checkboxes3 = QtWidgets.QHBoxLayout()  
        hbox_checkboxes4 = QtWidgets.QHBoxLayout()          
        hbox_apply_to = QtWidgets.QHBoxLayout()
        hbox_buttons1 = QtWidgets.QHBoxLayout()
        hbox_buttons2 = QtWidgets.QHBoxLayout()
        
        # SET WINDOW ATTRIBUTES
        self.setGeometry(500, 300, 400, 110)
        self.setWindowTitle('Find & Replace')
        
        # CREATE WIDGETS
        self.search_for_label = QtWidgets.QLabel("Search For:  ")
        self.search_for_line_edit = QtWidgets.QLineEdit()
        self.replace_with_label = QtWidgets.QLabel("Replace With:")
        self.replace_with_line_edit = QtWidgets.QLineEdit()
        self.search_in_node_names_checkbox = QtWidgets.QCheckBox("Search In Node Names")
        self.search_in_parameters_checkbox = QtWidgets.QCheckBox("Search In Parameters")
        self.include_string_parms_checkbox = QtWidgets.QCheckBox("Include String Parms")
        self.include_float_parms_checkbox = QtWidgets.QCheckBox("Include Float Parms")
        self.include_expressions_checkbox = QtWidgets.QCheckBox("Include Expressions")
        self.select_in_viewport_checkbox = QtWidgets.QCheckBox("Select In Viewport")
        self.print_results_checkbox = QtWidgets.QCheckBox("Print Results")        
        self.case_sensitive_checkbox = QtWidgets.QCheckBox("Case Sensitive")
        self.apply_to_label = QtWidgets.QLabel("Apply To:")
        self.apply_to_combo_box = QtWidgets.QComboBox(self)
        self.find_button = QtWidgets.QPushButton('Find', self)
        self.replace_button = QtWidgets.QPushButton('Replace', self)
        
        # POPULATE COMBO BOX
        self.apply_to_combo_box.addItem("Selected Nodes Only")
        self.apply_to_combo_box.addItem("Selected Nodes & Their Direct Children")
        self.apply_to_combo_box.addItem("Selected Nodes & All Subchildren")        
        self.apply_to_combo_box.addItem("Only Direct Children Of Selected Nodes")   
        self.apply_to_combo_box.addItem("Only All Subchildren Of Selected Nodes")           
        self.apply_to_combo_box.addItem("All Nodes In Obj Context")   
        self.apply_to_combo_box.addItem("All Nodes In Scene (Any Context)")           
        
        # SET INITIAL WIDGET BEHAVIORS
        self.search_in_node_names_checkbox.setCheckState(QtCore.Qt.Checked)
        self.search_in_parameters_checkbox.setCheckState(QtCore.Qt.Unchecked)
        self.case_sensitive_checkbox.setCheckState(QtCore.Qt.Unchecked)        
        self.select_in_viewport_checkbox.setCheckState(QtCore.Qt.Checked)  
        self.print_results_checkbox.setCheckState(QtCore.Qt.Unchecked)  
        self.include_string_parms_checkbox.setCheckState(QtCore.Qt.Checked)    
        self.include_float_parms_checkbox.setCheckState(QtCore.Qt.Checked)          
        self.include_expressions_checkbox.setCheckState(QtCore.Qt.Checked)
        self.include_string_parms_checkbox.setEnabled(False)
        self.include_float_parms_checkbox.setEnabled(False)
        self.include_expressions_checkbox.setEnabled(False)

        # WATCH WIDGETS FOR STATECHANGE
        self.search_for_line_edit.textChanged.connect(self.lineEditChanged)
        self.replace_with_line_edit.textChanged.connect(self.lineEditChanged)
        self.search_in_parameters_checkbox.stateChanged.connect(self.searchInParametersCheckboxChanged)
        self.search_in_node_names_checkbox.stateChanged.connect(self.searchInNodeNamesCheckboxChanged)
        self.include_string_parms_checkbox.stateChanged.connect(self.includeCheckboxChanged)
        self.include_float_parms_checkbox.stateChanged.connect(self.includeCheckboxChanged)
        self.include_expressions_checkbox.stateChanged.connect(self.includeCheckboxChanged)  
        self.print_results_checkbox.stateChanged.connect(self.printResultsUnchecked)          
        self.select_in_viewport_checkbox.stateChanged.connect(self.selectInViewportUnchecked)        
        self.apply_to_combo_box.currentIndexChanged.connect(self.comboBoxIndexChanged)
        
        # CONNECT BUTTONS TO FUNCTIONS
        self.find_button.clicked.connect(self.locate)
        self.replace_button.clicked.connect(self.locateAndReplace)

        # ADD WIDGETS TO LAYOUT
        hbox1.addWidget(self.search_for_label)
        hbox1.addWidget(self.search_for_line_edit)
        hbox2.addWidget(self.replace_with_label)
        hbox2.addWidget(self.replace_with_line_edit)
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)
        vbox.addLayout(hbox4)
        hbox_checkboxes1.addWidget(self.search_in_node_names_checkbox)
        hbox_checkboxes1.addWidget(self.search_in_parameters_checkbox)   
        
        hbox_checkboxes2.addWidget(self.case_sensitive_checkbox)           
        hbox_checkboxes2.addWidget(self.include_string_parms_checkbox)
        hbox_checkboxes3.addWidget(self.select_in_viewport_checkbox)     
        hbox_checkboxes3.addWidget(self.include_float_parms_checkbox)
        hbox_checkboxes4.addWidget(self.print_results_checkbox)    
        hbox_checkboxes4.addWidget(self.include_expressions_checkbox)            
        vbox.addLayout(hbox_checkboxes1)
        vbox.addLayout(hbox_checkboxes2) 
        vbox.addLayout(hbox_checkboxes3)
        vbox.addLayout(hbox_checkboxes4)        
        hbox_apply_to.addWidget(self.apply_to_label)        
        hbox_apply_to.addWidget(self.apply_to_combo_box)
        vbox.addLayout(hbox_apply_to)
        hbox_buttons1.addWidget(self.find_button)
        hbox_buttons1.addWidget(self.replace_button)
        vbox.addLayout(hbox_buttons1)           

        # SET LAYOUT
        self.setLayout(vbox)
        
    ## FUNCTION TO RUN WHEN LINEEDITS ARE CHANGED
    def lineEditChanged(self):
        try:
            if self.search_for_line_edit.text():
                int(self.search_for_line_edit.text())
            if self.replace_with_line_edit.text():
                int(self.replace_with_line_edit.text())
            if self.search_in_parameters_checkbox.isChecked():
                self.include_float_parms_checkbox.setEnabled(1)
            if self.find_button.isEnabled() == 0:
                self.find_button.setEnabled(1)
                self.replace_button.setEnabled(1)
        except:
            self.include_float_parms_checkbox.setEnabled(0)
            if self.include_string_parms_checkbox.isChecked() == 0 and self.include_expressions_checkbox.isChecked() == 0:
                if self.find_button.isEnabled() == 1:
                    self.find_button.setEnabled(0)
                    self.replace_button.setEnabled(0)


    ## FUNCTIONS TO RUN WHEN CHECKBOX STATES ARE CHANGED        
    def searchInParametersCheckboxChanged(self, state):
        if state == QtCore.Qt.Checked:
            self.search_in_node_names_checkbox.setCheckState(QtCore.Qt.Unchecked)     
            self.include_string_parms_checkbox.setEnabled(1)
            self.include_expressions_checkbox.setEnabled(1)
            self.include_float_parms_checkbox.setEnabled(1)
        else:
            self.search_in_node_names_checkbox.setCheckState(QtCore.Qt.Checked)  
            self.include_string_parms_checkbox.setEnabled(0)
            self.include_expressions_checkbox.setEnabled(0)
            self.include_float_parms_checkbox.setEnabled(0)

    def searchInNodeNamesCheckboxChanged(self, state):
        if state == QtCore.Qt.Checked:
            self.search_in_parameters_checkbox.setCheckState(QtCore.Qt.Unchecked)   
            self.include_string_parms_checkbox.setEnabled(0)
            self.include_expressions_checkbox.setEnabled(0)
            self.include_float_parms_checkbox.setEnabled(0)
            self.find_button.setEnabled(1)
            self.replace_button.setEnabled(1)
        else:
            self.search_in_parameters_checkbox.setCheckState(QtCore.Qt.Checked)        
            self.include_string_parms_checkbox.setEnabled(1)
            self.include_expressions_checkbox.setEnabled(1)
            self.include_float_parms_checkbox.setEnabled(1)
            if self.include_string_parms_checkbox.checkState() == QtCore.Qt.Unchecked and self.include_float_parms_checkbox.checkState() == QtCore.Qt.Unchecked and self.include_expressions_checkbox.checkState() == QtCore.Qt.Unchecked:
                self.find_button.setEnabled(0)
                self.replace_button.setEnabled(0)                
            
    def includeCheckboxChanged(self, state):
            include_string_parms = self.include_string_parms_checkbox.checkState()         
            include_float_parms = self.include_float_parms_checkbox.checkState()
            include_expressions = self.include_expressions_checkbox.checkState()
            if include_string_parms == QtCore.Qt.Unchecked and include_float_parms == QtCore.Qt.Unchecked and include_expressions == QtCore.Qt.Unchecked:
                if self.find_button.isEnabled() == 1:
                    self.find_button.setEnabled(0)
                    self.replace_button.setEnabled(0)
            elif include_string_parms == QtCore.Qt.Unchecked and include_expressions == QtCore.Qt.Unchecked and self.include_float_parms_checkbox.isEnabled() == 0:
                if self.find_button.isEnabled() == 1:
                    self.find_button.setEnabled(0)
                    self.replace_button.setEnabled(0)            
            else:
                if self.find_button.isEnabled() == 0:
                    self.find_button.setEnabled(1)
                    self.replace_button.setEnabled(1)    
                    
    def selectInViewportUnchecked(self, state):
            if state == QtCore.Qt.Unchecked:
                self.print_results_checkbox.setCheckState(QtCore.Qt.Checked)
                
    def printResultsUnchecked(self, state):
            if state == QtCore.Qt.Unchecked:
                self.select_in_viewport_checkbox.setCheckState(QtCore.Qt.Checked)        
                
    ## FUNCTION TO RUN WHEN COMBO BOX IS CHANGED
    def comboBoxIndexChanged(self):
        index = self.apply_to_combo_box.currentIndex()
        if index != 0:
            self.select_in_viewport_checkbox.setEnabled(0)
        else:
            self.select_in_viewport_checkbox.setEnabled(1)
            
    ## FUNCTION THAT IS RUN WHEN "FIND" BUTTON IS PRESSED
    def locate(self):
        
        # INITIALIZE VARIABLES
        search_string = self.search_for_line_edit.text()    
        current_selection = list( hou.selectedNodes() )
        sel = self.setSearchMode(current_selection)
        found_node_list = []

        # SEARCH IN NODE NAMES AND BUILD LIST 
        if self.search_in_node_names_checkbox.checkState() == QtCore.Qt.Checked:
            for node in sel:
                
                # IF "SELECT IN VIEWPORT" IS ENABLED, DESELECT CURRENT SELECTION                
                if self.select_in_viewport_checkbox.checkState() == QtCore.Qt.Checked and self.select_in_viewport_checkbox.isEnabled():
                    node.setSelected(0)
                    
                # APPEND TO LIST, WITH CASE SENSITIVE CHECK
                if self.checkCaseSensitive(search_string) in self.checkCaseSensitive(node.name()):
                    found_node_list.append(node)

        # SEARCH IN PARAMETERS AND BUILD LIST
        if self.search_in_parameters_checkbox.checkState() == QtCore.Qt.Checked:
            for node in sel:
                
                # IF "SELECT IN VIEWPORT" IS ENABLED, DESELECT CURRENT SELECTION                
                if self.select_in_viewport_checkbox.checkState() == QtCore.Qt.Checked and self.select_in_viewport_checkbox.isEnabled():
                    node.setSelected(0)   
                    
                #ITERATE OVER ALL PARMS OF NODE
                for p in node.parms():
                    
                    # IF STRING PARM OPTION IS ENABLED, APPEND TO LIST, WITH CASE SENSITIVE CHECK
                    if type(p.parmTemplate()) is hou.StringParmTemplate:  
                        if self.include_string_parms_checkbox.checkState()  == QtCore.Qt.Checked:                    
                            if self.checkCaseSensitive(search_string) in self.checkCaseSensitive(str(p.eval())):
                                found_node_list.append(node)
                                break
                    
                    # FLOAT PARM OPTION IS ENABLED, APPEND TO LIST, WITH CASE SENSITIVE CHECK
                    if type(p.parmTemplate()) is hou.FloatParmTemplate:
                        if self.include_float_parms_checkbox.checkState() == QtCore.Qt.Checked and self.include_float_parms_checkbox.isEnabled():                    
                            if self.checkCaseSensitive(search_string) in self.checkCaseSensitive(str(p.eval())):
                                found_node_list.append(node)
                                break
                    
                    # EXPRESSION OPTION IS ENABLED, APPEND TO LIST, WITH CASE SENSITIVE CHECK
                    if self.include_expressions_checkbox.checkState() == QtCore.Qt.Checked:
                        if p.keyframes():
                            if self.checkCaseSensitive(search_string) in self.checkCaseSensitive(str(p.expression())):
                                found_node_list.append(node)
                                break
        
        # IF MATCHES WERE FOUND, PRINT RESULTS IF ENABLED, AND SELECT IN VIEWPORT IF ENABLED
        if found_node_list:
            
            if self.print_results_checkbox.checkState() == QtCore.Qt.Checked:
                print("The following nodes met the search criteria:")
                
            for node in found_node_list:    
                if self.select_in_viewport_checkbox.checkState() == QtCore.Qt.Checked and self.select_in_viewport_checkbox.isEnabled():
                    node.setSelected(1)
                    
                if self.print_results_checkbox.checkState() == QtCore.Qt.Checked:
                    print(node.path())
            if self.print_results_checkbox.checkState() == QtCore.Qt.Checked:
                print("\n")
                
        # IF NO MATCHES WERE FOUND, PRINT INFO
        else:
            if self.print_results_checkbox.checkState() == QtCore.Qt.Checked:
                print("No nodes were found which met the search criteria.\n")
                                
    ## FUNCTION THAT IS RUN WHEN "REPLACE" BUTTON IS PRESSED                
    def locateAndReplace(self):
        
        # INITIALIZE VARIABLES        
        to_replace = self.search_for_line_edit.text()
        replace_with = self.replace_with_line_edit.text()
        include_string_parms = self.include_string_parms_checkbox.checkState() 
        include_float_parms = self.include_float_parms_checkbox.checkState()  
        include_expressions = self.include_expressions_checkbox.checkState()             
        current_selection = list( hou.selectedNodes() )
        sel = self.setSearchMode(current_selection)

        # IF NODE SEARCH IS ENABLED AND NAME MATCHES, REPLACE NAME, WITH CASE SENSITIVE CHECK 
        if self.search_in_node_names_checkbox.checkState() == QtCore.Qt.Checked:
            for node in sel:
                if self.checkCaseSensitive(to_replace) in self.checkCaseSensitive(node.name()):
                    self.replaceFunction(0, to_replace, replace_with, node)

        # IF PARAMETER SEARCH IS ENABLED, ITERATE OVER ALL PARAMETERS IN SELECTED NODES
        if self.search_in_parameters_checkbox.checkState() == QtCore.Qt.Checked and self.search_in_parameters_checkbox.isEnabled():
            for node in sel:
                for p in node.parms():

                    # IF EXPRESSIONS ARE ENABLED
                    if include_expressions == QtCore.Qt.Checked:
                        x = 0
                        
                        # IF KEYFRAMED, ITERATE OVER KEYFRAMES AND REPLACE EXPRESSION IF MATCHED, WITH CASE SENSITIVE CHECK
                        if p.keyframes():
                            for keyframe in p.keyframes():
                                if self.checkCaseSensitive(to_replace) in self.checkCaseSensitive(p.keyframes()[x].expression()):
                                    self.replaceFunction(3, to_replace, replace_with, p) 
                                    x += 1
                                    continue
                                    
                        # OTHERWISE IF IT IS A STRING PARM, REPLACE STRING IF MATCHED, WITH CASE SENSITIVE CHECK
                        elif type(p.parmTemplate()) is hou.StringParmTemplate:                           
                            if self.checkCaseSensitive(to_replace) in self.checkCaseSensitive(p.unexpandedString()):
                                self.replaceFunction(4, to_replace, replace_with, p) 
                                x += 1
                                continue

                    # IF STRING PARMS ARE ENABLED, REPLACE STRING IF MATCHED, WITH CASE SENSITIVE CHECK
                    if type(p.parmTemplate()) is hou.StringParmTemplate:
                        if include_string_parms == QtCore.Qt.Checked:
                            if self.checkCaseSensitive(to_replace) in self.checkCaseSensitive(p.eval()):           
                                self.replaceFunction(1, to_replace, replace_with, p)           
                                continue
  
                    # IF STRING PARMS ARE ENABLED, REPLACE FLOAT IF MATCHED, WITH CASE SENSITIVE CHECK
                    if type(p.parmTemplate()) is hou.FloatParmTemplate:
                        if include_float_parms == QtCore.Qt.Checked and self.include_float_parms_checkbox.isEnabled():
                            try:
                                if str(float(to_replace)) in str(p.eval()):       
                                    self.replaceFunction(2, to_replace, replace_with, p)  
                                    continue
                            except:
                                pass

        if self.print_results_checkbox.checkState() == QtCore.Qt.Checked:
            print("\n")
    
    # FUNCTION TO REPLACE WITH CASE SENSITIVITY TAKEN INTO ACCOUNT
    def replaceFunction(self, replace_mode, to_replace, replace_with, input): 
        
        # IF WE'RE MODIFYING A NODE NAME
        if replace_mode == 0:
            self.modifyNodeName(to_replace, replace_with, input)

        # IF WE'RE MODIFYING A STRING PARM
        elif replace_mode == 1:
            self.modifyStringParm(to_replace, replace_with, input)
                
        # IF WE'RE MODIFYING A FLOAT PARM, SIMPLY REPLACE SEARCH VALUE WITH REPLACE VALUE
        elif replace_mode == 2:
            self.modifyFloatParm(to_replace, replace_with, input)

        # IF WE'RE MODIFYING AN EXPRESSION
        elif replace_mode == 3:
            self.modifyExpression(to_replace, replace_with, input)

        # IF WE'RE MODIFYING AN EXPRESSION WITH `CHS` (ISN'T TREATED AS EXPRESSION BY PYTHON)
        elif replace_mode == 4:
            self.modifyChs(to_replace, replace_with, input)
                    
                
    ## MODIFY NODE NAME                 
    def modifyNodeName(self, to_replace, replace_with, input):
        node = input
        old_node_path = node.path()

        # IF CASE SENSITIVE
        if self.case_sensitive_checkbox.checkState() == QtCore.Qt.Checked:
            node.setName(node.name().replace(to_replace, replace_with),1)
            if self.print_results_checkbox.checkState() == QtCore.Qt.Checked:
                print('Updating node name from "{0}" to "{1}"'.format(old_node_path, node.path()))

        # IF NOT CASE SENSITIVE
        else:
            compare_string = node.name()
            index_list = []
            index = 0

            # SEARCH FOR MATCH, FINDING INDEX TO REPLACE                
            if to_replace.lower() in compare_string.lower():
                for ch in compare_string.lower():
                    if ch == to_replace[0].lower():
                        if compare_string.lower()[index:index+len(to_replace)] == to_replace.lower():
                            index_list.append(index)
                index += 1

            # REPLACE STRING BY INDEX                    
            for index in index_list:
                node.setName(compare_string.replace(compare_string[index:index+len(to_replace)], replace_with))

            if self.print_results_checkbox.checkState() == QtCore.Qt.Checked:            
                print('Updating node name from "{0}" to "{1}"'.format(old_node_path, node.path()))
                    
    ## MODIFY STRING PARAMETER
    def modifyStringParm(self, to_replace, replace_with, input):
            p = input
            old_parm_path = p.path()
            old_parm_val = p.eval()
            
            # IF CASE SENSITIVE, SIMPLY REPLACE SEARCH STRING WITH REPLACE STRING
            if self.case_sensitive_checkbox.checkState() == QtCore.Qt.Checked:
                p.set(p.eval().replace(to_replace,replace_with))
                if self.print_results_checkbox.checkState() == QtCore.Qt.Checked:            
                    print('Updating "{0}" from "{1}" to "{2}"'.format(old_parm_path, old_parm_val, p.eval()))
                    
            # IF NOT CASE SENSITIVE
            else:
                compare_string = p.eval()
                diff = len(replace_with)-len(to_replace)
                index_list = []
                index = 0
                
                # SEARCH FOR MATCH, FINDING INDEX TO REPLACE
                if to_replace.lower() in compare_string.lower():
                    for ch in compare_string.lower():                        
                        if ch == to_replace[0].lower():
                            if compare_string.lower()[index:index+len(to_replace)] == to_replace.lower():
                                index_list.append(index)
                        index += 1
                index_list.sort()
                iter = 0
                
                # REPLACE STRING BY INDEX
                for index in index_list:
                    updated_index = index + (iter * diff)
                    iter += 1
                    new_replace = compare_string[updated_index:updated_index+len(to_replace)]
                    compare_string = compare_string.replace(new_replace, replace_with)
                    p.set(compare_string)
                    if self.print_results_checkbox.checkState() == QtCore.Qt.Checked:            
                        print('Updating "{0}" from "{1}" to "{2}"'.format(old_parm_path, old_parm_val, p.eval()))
    
    ## MODIFY FLOAT PARM
    def modifyFloatParm(self, to_replace, replace_with, input):
            p = input
            old_parm_path = p.path()
            old_parm_val = p.eval()
            p.set(float(str(p.eval()).replace(str(float(to_replace)),replace_with)))
            if self.print_results_checkbox.checkState() == QtCore.Qt.Checked:            
                print('Updating {0} from "{1}" to "{2}"' % (old_parm_path, old_parm_val, p.eval()))
                
    ## MODIFY EXPRESSION
    def modifyExpression(self, to_replace, replace_with, input):
            p = input
            old_parm_path = p.path()
            x = 0
            for keyframe in p.keyframes():
                new_keyframe = hou.Keyframe()
                new_keyframe.setFrame( keyframe.frame() )
                old_parm_val = p.keyframes()[x].expression()  

            # IF CASE SENSITIVE
            if self.case_sensitive_checkbox.checkState() == QtCore.Qt.Checked:           
                new_keyframe.setExpression( p.keyframes()[x].expression().replace(to_replace,replace_with) )
                p.setKeyframe(new_keyframe)
                if self.print_results_checkbox.checkState() == QtCore.Qt.Checked:            
                    print('Updating {0} from "{1}" to "{2}"'.format(old_parm_path, old_parm_val, p.keyframes()[x].expression() ))
                
            # IF NOT CASE SENSITIVE
            else:
                compare_string = p.keyframes()[x].expression()  
                diff = len(replace_with)-len(to_replace)
                index_list = []
                index = 0
                if to_replace.lower() in compare_string.lower():
                    for ch in compare_string.lower():                        
                        if ch == to_replace[0].lower():
                            if compare_string.lower()[index:index+len(to_replace)] == to_replace.lower():
                                index_list.append(index)
                            index += 1
                index_list.sort()
                iter = 0
                new_replace_list = []
                for index in index_list:
                    new_replace = compare_string[index:index+len(to_replace)]
                    new_replace_list.append(new_replace)
                new_replace_list = list(set(new_replace_list))
                for new_replace in new_replace_list:
                    new_keyframe.setExpression( compare_string.replace(new_replace, replace_with) )
                    p.setKeyframe(new_keyframe)
                    if self.print_results_checkbox.checkState() == QtCore.Qt.Checked:            
                        print('Updating "{0}" from "{1}" to "{2}"'.format(old_parm_path, old_parm_val, p.keyframes()[x].expression() ))
                x += 1                         
                
    ## MODIFY EXPRESSION WITH 'chs('
    def modifyChs(self, to_replace, replace_with, input):
            p = input
            old_parm_path = p.path()
            x = 0
            old_parm_val = p.unexpandedString()

            p.setExpression('')
            p.deleteAllKeyframes()

            # IF CASE SENSITIVE
            if self.case_sensitive_checkbox.checkState() == QtCore.Qt.Checked:      
                new_parm_val = old_parm_val.replace(to_replace,replace_with)
                p.set(new_parm_val)
                if self.print_results_checkbox.checkState() == QtCore.Qt.Checked:            
                    print('Updating {0} from "{1}" to "{2}"'.format(old_parm_path, old_parm_val, new_parm_val ))
                    
            # IF NOT CASE SENSITIVE
            else:
                compare_string = old_parm_val 
                diff = len(replace_with)-len(to_replace)
                index_list = []
                index = 0
                if to_replace.lower() in compare_string.lower():
                    for ch in compare_string.lower():                        
                        if ch == to_replace[0].lower():
                            if compare_string.lower()[index:index+len(to_replace)] == to_replace.lower():
                                index_list.append(index)
                        index += 1
                index_list.sort()
                iter = 0
                new_replace_list = []
                for index in index_list:
                    new_replace = compare_string[index:index+len(to_replace)]
                    new_replace_list.append(new_replace)
                new_replace_list = list(set(new_replace_list))
                for new_replace in new_replace_list:
                    new_parm_val = compare_string.replace(new_replace, replace_with)
                    p.set( new_parm_val )
                    if self.print_results_checkbox.checkState() == QtCore.Qt.Checked:            
                        print('Updating "{0}" from "{1}" to "{2}"' % (old_parm_path, old_parm_val, new_parm_val ))
                x += 1                                
                    
    ## CREATES LOWERCASE VERSION OF INPUT IF 'CASE SENSITIVE' IS DESELECTED    
    def checkCaseSensitive(self, input):
        if self.case_sensitive_checkbox.checkState() == QtCore.Qt.Unchecked:
            input = input.lower()
        return input
        
    ## MODIFIES THE SELECTED NODE LIST BASED ON "APPLY TO:" COMBO BOX
    def setSearchMode(self, current_selection):
        search_mode = self.apply_to_combo_box.currentIndex() 

        # SELECTED NODES ONLY
        if search_mode == 0:
            sel = current_selection

        # SELECTED NODES AND DIRECT CHILDREN
        elif search_mode == 1:
            sel = []
            for node in current_selection:
                if node.children():
                    sel.extend(list(node.children()))   
            sel.extend(current_selection)

        # SELECTED NODES & ALL SUBCHILDREN
        elif search_mode == 2:
            sel = current_selection
            for node in current_selection:
                if node.children():
                    sel.extend(list(node.allSubChildren()))

        # ONLY DIRECT CHILDREN OF SELECTED NODES
        elif search_mode == 3:
            sel = []
            for node in current_selection:
                if node.children():
                    sel.extend(list(node.children()))

        # ONLY ALL SUBCHILDREN OF SELECTED NODES
        elif search_mode == 4:
            sel = []
            for node in current_selection:
                if node.children():
                    sel.extend(node.allSubChildren())   

        # ALL NODES IN OBJ CONTEXT
        elif search_mode == 5:
            sel = []
            for node in hou.node('/obj').allSubChildren():
                if "/obj/ipr_camera" not in node.path():
                    sel.append(node)

        # ALL NODES IN SCENE (ANY CONTEXT)
        elif search_mode == 6:
            sel = []
            for node in hou.node('/').allSubChildren():
                if "/obj/ipr_camera" not in node.path():
                    sel.append(node)    

        return sel                
    
## RUN DIALOG                  
dialog = findAndReplace()
dialog.show()
