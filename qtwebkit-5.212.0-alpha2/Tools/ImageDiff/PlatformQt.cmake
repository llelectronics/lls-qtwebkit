set(IMAGE_DIFF_SOURCES
    ${IMAGE_DIFF_DIR}/qt/ImageDiff.cpp
)

list(APPEND IMAGE_DIFF_SYSTEM_INCLUDE_DIRECTORIES
    ${Qt5Gui_INCLUDE_DIRS}
)

set(IMAGE_DIFF_LIBRARIES
    ${Qt5Gui_LIBRARIES}
)
