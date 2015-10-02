#!/usr/bin/python
#coding=utf8
##----------------------------------------------------------------------------##
##               █      █                                                     ##
##               ████████                                                     ##
##             ██        ██                                                   ##
##            ███  █  █  ███                                                  ##
##            █ █        █ █        framemerger.py                            ##
##             ████████████         frame-merger                              ##
##           █              █       Copyright (c) 2015 AmazingCow             ##
##          █     █    █     █      www.AmazingCow.com                        ##
##          █     █    █     █                                                ##
##           █              █       N2OMatt - n2omatt@amazingcow.com          ##
##             ████████████         www.amazingcow.com/n2omatt                ##
##                                                                            ##
##                                                                            ##
##                  This software is licensed as GPLv3                        ##
##                 CHECK THE COPYING FILE TO MORE DETAILS                     ##
##                                                                            ##
##    Permission is granted to anyone to use this software for any purpose,   ##
##   including commercial applications, and to alter it and redistribute it   ##
##               freely, subject to the following restrictions:               ##
##                                                                            ##
##     0. You **CANNOT** change the type of the license.                      ##
##     1. The origin of this software must not be misrepresented;             ##
##        you must not claim that you wrote the original software.            ##
##     2. If you use this software in a product, an acknowledgment in the     ##
##        product IS HIGHLY APPRECIATED, both in source and binary forms.     ##
##        (See opensource.AmazingCow.com/acknowledgment.html for details).    ##
##        If you will not acknowledge, just send us a email. We'll be         ##
##        *VERY* happy to see our work being used by other people. :)         ##
##        The email is: acknowledgmentopensource@AmazingCow.com               ##
##     3. Altered source versions must be plainly marked as such,             ##
##        and must notbe misrepresented as being the original software.       ##
##     4. This notice may not be removed or altered from any source           ##
##        distribution.                                                       ##
##     5. Most important, you must have fun. ;)                               ##
##                                                                            ##
##      Visit opensource.amazingcow.com for more open-source projects.        ##
##                                                                            ##
##                                  Enjoy :)                                  ##
##----------------------------------------------------------------------------##

## Imports ##
import os;
import os.path;
import sys;
import getopt;
import termcolor;
#COWTODO: Today we're using pygame to merge the photos.
#COWTODO: But the desired is to use ImageMagick...
import pygame;
#For GUI :)
from PyQt4.QtCore import *
from PyQt4.QtGui  import *

################################################################################
## Constants                                                                  ##
################################################################################
class Constants:
    #Flag.
    FLAG_HELP             = "h", "help";
    FLAG_VERSION          = "v", "version";
    FLAG_GUI              = "" , "gui";
    FLAG_FRAME_IMAGE_PATH = "f", "frame";
    FLAG_IMAGES_DIR_PATH  = "i", "images-dir";
    FLAG_OUTPUT_DIR_PATH  = "o", "output-dir";

    ALL_FLAGS_SHORT = "hvf:i:o:";
    ALL_FLAGS_LONG  = [
        FLAG_HELP            [1],
        FLAG_VERSION         [1],
        FLAG_GUI             [1],
        FLAG_FRAME_IMAGE_PATH[1] + "=",
        FLAG_IMAGES_DIR_PATH [1] + "=",
        FLAG_OUTPUT_DIR_PATH [1] + "="
    ];

    #Image formats.
    IMAGE_FORMATS = [".png", ".jpg", ".jpeg"];

    #App.
    APP_NAME      = "frame-merger";
    APP_VERSION   = "0.1.0";
    APP_AUTHOR    = "N2OMatt <n2omatt@amazingcow.com>"
    APP_COPYRIGHT = "\n".join(("Copyright (c) 2015 - Amazing Cow",
                               "This is a free software (GPLv3) - Share/Hack it",
                               "Check opensource.amazingcow.com for more :)"));



################################################################################
## GUI                                                                        ##
################################################################################
class GUI(QWidget):
    ############################################################################
    ## Static Run Method                                                      ##
    ############################################################################
    @staticmethod
    def run():
        app = QApplication(sys.argv);
        gui = GUI();
        gui.show();
        sys.exit(app.exec_())


    ############################################################################
    ## CTOR                                                                   ##
    ############################################################################
    def __init__(self):
        QWidget.__init__(self);

        #Create the widgets.
        self.frame_image_label  = None;
        self.frame_image_text   = None;
        self.frame_image_button = None;

        self.images_dir_label  = None;
        self.images_dir_text   = None;
        self.images_dir_button = None;

        self.output_dir_label  = None;
        self.output_dir_text   = None;
        self.output_dir_button = None;

        self.run_button = None;

        #Create the layout.
        self.root_layout = None;

        #Start the ui.
        self.init_ui();


    ############################################################################
    ## UI Initializer                                                         ##
    ############################################################################
    def init_ui(self):
        #Set the window properties.
        self.setWindowTitle("{} - {} - {}".format(Constants.APP_NAME,
                                                  Constants.APP_VERSION,
                                                  "Amazing Cow"));
        #Set the window properties.
        self.setGeometry(0, 0, 480, 200);

        #Create the widgets.
        #Frame Image.
        self.frame_image_label = QLabel("Frame Image Path:");

        self.frame_image_text = QLineEdit();
        self.frame_image_text.textChanged.connect(self.on_text_changed);

        self.frame_image_button = QPushButton("...");
        self.frame_image_button.clicked.connect(self.on_frame_image_button_pressed);

        #Images Dir.
        self.images_dir_label = QLabel("Images Directory Path:");

        self.images_dir_text  = QLineEdit();
        self.images_dir_text.textChanged.connect(self.on_text_changed);

        self.images_dir_button = QPushButton("...");
        self.images_dir_button.clicked.connect(self.on_images_dir_button_pressed);

        #Ouput Dir.
        self.output_dir_label = QLabel("Output Directory Path:");

        self.output_dir_text  = QLineEdit();
        self.output_dir_text.textChanged.connect(self.on_text_changed);

        self.output_dir_button = QPushButton("...");
        self.output_dir_button.clicked.connect(self.on_output_dir_button_pressed);

        #Run Button.
        self.run_button = QPushButton("Start merge!");
        self.run_button.setEnabled(True);
        self.run_button.clicked.connect(self.on_run_button_pressed);

        #Create the layout.
        self.root_layout = QGridLayout(self);

        #Add the widgets to layout.
        #Frame Image.
        self.root_layout.addWidget(self.frame_image_label,  1, 1);
        self.root_layout.addWidget(self.frame_image_text,   2, 1);
        self.root_layout.addWidget(self.frame_image_button, 2, 2);
        #Images Dir.
        self.root_layout.addWidget(self.images_dir_label,  3, 1);
        self.root_layout.addWidget(self.images_dir_text,   4, 1);
        self.root_layout.addWidget(self.images_dir_button, 4, 2);
        #Output Dir.
        self.root_layout.addWidget(self.output_dir_label,  5, 1);
        self.root_layout.addWidget(self.output_dir_text,   6, 1);
        self.root_layout.addWidget(self.output_dir_button, 6, 2);
        #Merge Button.
        self.root_layout.addWidget(self.run_button, 7, 1, 2, 1 );


    ############################################################################
    ## Button Callbacks                                                       ##
    ############################################################################
    def on_frame_image_button_pressed(self):
        #Create a string with the supported image formats to pass to QFileDialog.
        #The string will have the format of Images Files (*.FMT1 *.FMT2 *.FMTN)
        #This is need to ensure that user will selected a valid image format.
        image_formats_str = "Image Files (*{})".format(" *".join(Constants.IMAGE_FORMATS));
        file_selected = QFileDialog.getOpenFileName(self,
                                                    "Select Frame Image",
                                                    "",
                                                    image_formats_str);

        self.frame_image_text.setText(file_selected);

    def on_images_dir_button_pressed(self):
        #COWTODO: Comment.
        dir_selected = QFileDialog.getExistingDirectory(self,
                                                        "Select Images Directory",
                                                        "",
                                                        QFileDialog.ShowDirsOnly);
        self.images_dir_text.setText(dir_selected);

    def on_output_dir_button_pressed(self):
        #COWTODO: Comment.
        dir_selected = QFileDialog.getExistingDirectory(self,
                                                        "Select Ouput Directory",
                                                        "",
                                                        QFileDialog.ShowDirsOnly);
        self.output_dir_text.setText(dir_selected);

    def on_run_button_pressed(self):
        #COWTODO: Comment.
        try:
            #Create and setup the MergeProcess..
            merge_process = MergeProcess();

            merge_process.set_frame_path (str(self.frame_image_text.text()));
            merge_process.set_images_path(str(self.images_dir_text.text ()));
            merge_process.set_output_path(str(self.output_dir_text.text ()));

            merge_process.init();


            #Create the progress dialog.
            progress = QProgressDialog("Merging Photos",
                                       "Cancel",
                                       0,
                                       merge_process.get_images_count(),
                                       self);
            progress.setWindowModality(Qt.WindowModal);


            #Keep merging the photos and updating the progress interface
            #until all photos are merged or user wants to quit.
            while(merge_process.has_image_to_merge()):
                merge_process.merge();
                progress.setValue(merge_process.get_current_image_index());

                #User wants to quit.
                if(progress.wasCanceled()): return;

            #Set the all things are done.
            progress.setValue(merge_process.get_images_count());

            #Show to user that processing was complete.
            QMessageBox.information(self,
                                    "Frame Merger",
                                    "Processing complete...",
                                    QMessageBox.Ok);

        #COWTODO: Comment.
        except Exception, e:
            QMessageBox. critical(self,
                                  "Frame Merger",
                                  str(e),
                                  QMessageBox.Ok);


    ############################################################################
    ## Text Box Callbacks                                                     ##
    ############################################################################
    def on_text_changed(self):
        #COWTODO: Comment.
        frame_len  = len(self.frame_image_text.text());
        images_len = len(self.images_dir_text.text());
        output_len = len(self.output_dir_text.text());

        all_filled = frame_len != 0 and images_len != 0 and output_len != 0;
        self.run_button.setEnabled(all_filled);



################################################################################
## MergeProcess                                                               ##
################################################################################
class MergeProcess:
    ############################################################################
    ## CTOR                                                                   ##
    ############################################################################
    def __init__(self):
        #COWTODO: Comment.
        self.__frame_path  = None;
        self.__images_path = None;
        self.__output_path = None;

        self.__images_filenames     = None;
        self.__current_photo_index  = 0;

    ############################################################################
    ## Initializer Method                                                     ##
    ############################################################################
    def init(self):
        #COWTODO: Comment.
        self.__check_paths();
        self.__clean_images_filenames_list();


    ############################################################################
    ## Path Setters                                                           ##
    ############################################################################
    def set_frame_path(self, path):
        self.__frame_path = path;

    def set_images_path(self, path):
        self.__images_path = path;

    def set_output_path(self, path):
        self.__output_path = path;


    ############################################################################
    ## Merge Process State Getters                                            ##
    ############################################################################
    def get_images_count(self):
        return len(self.__images_filenames);

    def get_current_image_index(self):
        return self.__current_photo_index;

    def has_image_to_merge(self):
        return self.__current_photo_index < self.get_images_count();


    ############################################################################
    ## Action Method                                                          ##
    ############################################################################
    def merge(self):
        #COWTODO: Comment.
        image_filename = self.__images_filenames[self.__current_photo_index];

        image_fullpath  = os.path.join(self.__images_path, image_filename);
        output_fullpath = os.path.join(self.__output_path, image_filename);

        self.__merge_photo(image_fullpath, output_fullpath);

        self.__current_photo_index += 1;

    ############################################################################
    ## Helper Methods                                                         ##
    ############################################################################
    def __check_paths(self):
        #COWTODO: Comment.
        #Canonize the paths...
        self.__frame_path  = self.__canonize_path(self.__frame_path);
        self.__images_path = self.__canonize_path(self.__images_path);
        self.__output_path = self.__canonize_path(self.__output_path);

        #COWTODO: Comment.
        if(self.__frame_path is None or not os.path.isfile(self.__frame_path)):
            raise Exception("Frame Image Path is not a valid.");

        if(self.__images_path is None or not os.path.isdir(self.__images_path)):
            raise Exception("Images Dir Path is not a valid.");

        if(self.__output_path is None):
            raise Exception("Output Dir Path is not a valid.");

    def __canonize_path(self, path):
        if(path is None): return None;

        return os.path.abspath(os.path.expanduser(path));

    def __clean_images_filenames_list(self):
        #COWTODO: Comment.
        clean_filenames = [];

        #COWTODO: Comment.
        filenames = os.listdir(self.__images_path);
        for filename in filenames:
            name, ext = os.path.splitext(filename);
            if(ext in Constants.IMAGE_FORMATS):
                clean_filenames.append(filename);

        self.__images_filenames = clean_filenames;


    def __merge_photo(self, input_filename, output_filename):
        #COWTODO: Comment.
        try:
            frame_surface = pygame.image.load(self.__frame_path);
            image_surface = pygame.image.load(input_filename);

            image_surface.blit(frame_surface, (0,0));

            pygame.image.save(image_surface, output_filename);

        #COWTODO: Comment.
        except Exception, e:
            msg = "{} ({}) - Exception: {}".format("Error while merging photo",
                                                   input_filename,
                                                   str(e))
            raise Exception(msg);



################################################################################
## Color Functions                                                            ##
################################################################################
class C:
    @staticmethod
    def red(msg)    : return termcolor.colored(msg, "red");
    @staticmethod
    def green(msg)  : return termcolor.colored(msg, "green");
    @staticmethod
    def blue(msg)   : return termcolor.colored(msg, "blue");
    @staticmethod
    def magenta(msg): return termcolor.colored(msg, "magenta");
    @staticmethod
    def yellow(msg) : return termcolor.colored(msg, "yellow");


################################################################################
## Print Functions                                                            ##
################################################################################
def print_help():
    #COWTODO: Implement.
    help = """Usage:
  """;
    print help;
    exit(0);

def print_version():
    print "{} - {} - {}".format(Constants.APP_NAME,
                                Constants.APP_VERSION,
                                Constants.APP_AUTHOR);
    print Constants.APP_COPYRIGHT;
    print;
    exit(0);

def print_fatal(msg):
    print C.red("[FATAL]"), msg;
    exit(1);


################################################################################
## Helper Functions                                                           ##
################################################################################
def system_cmd(cmd, expected_ret_val = 0):
    #COWTODO: Comment.
    ret = os.system(cmd);
    if(ret != expected_ret_val):
        print_fatal("cmd:", cmd);

def run(frame_path, images_path, output_path):
    #COWTODO: Comment.
    try:
        merge_process = MergeProcess();

        merge_process.set_frame_path (frame_path);
        merge_process.set_images_path(images_path);
        merge_process.set_output_path(output_path);

        merge_process.init();

        print "Images found: {}".format(merge_process.get_images_count());
        while(merge_process.has_image_to_merge()):
            print "{} ({}) of ({})".format("Merging image",
                                            merge_process.get_current_image_index() + 1,
                                            merge_process.get_images_count());
            merge_process.merge();
        print "Done...";

    #COWTODO: Comment.
    except Exception, e:
        print_fatal(str(e));


################################################################################
## Script Initialization                                                      ##
################################################################################
def main():
    #Get the command line options.
    try:
        options = getopt.gnu_getopt(sys.argv[1:],
                                    Constants.ALL_FLAGS_SHORT,
                                    Constants.ALL_FLAGS_LONG);
    except Exception, e:
        print_fatal(e);

    #COWTODO: Comment.
    opt_frame_image_path = None;
    opt_images_dir_path  = None;
    opt_output_dir_path  = None;

    #Parse the options.
    for option in options[0]:
        key, value = option;
        key = key.lstrip("-");

        #Help/Version. - EXCLUSIVE OPTIONS : Run and quit.
        if  (key in Constants.FLAG_HELP   ): print_help();
        elif(key in Constants.FLAG_VERSION): print_version();

        #GUI - EXCLUSIVE OPTION : Run and quit.
        elif(key in Constants.FLAG_GUI):
            GUI.run();
            exit(0);

        #NON EXCLUSIVE OPTIONS : Grab the info to use later.
        #Frame and Images path.
        elif(key in Constants.FLAG_FRAME_IMAGE_PATH):
             opt_frame_image_path = value;
        elif(key in Constants.FLAG_IMAGES_DIR_PATH):
             opt_images_dir_path = value;
        #Output path.
        elif(key in Constants.FLAG_OUTPUT_DIR_PATH):
            opt_output_dir_path = value;

    #Will run in text mode.
    run(opt_frame_image_path,
        opt_images_dir_path,
        opt_output_dir_path);

if(__name__ == "__main__"):
    main();
