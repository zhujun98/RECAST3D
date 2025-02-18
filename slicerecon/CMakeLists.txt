project(slicerecon LANGUAGES CXX)

# Caveat: sequence
set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} "${CMAKE_CURRENT_SOURCE_DIR}/cmake")
find_package(FFTW REQUIRED COMPONENTS FLOAT_LIB)

find_package(Eigen3 3.3 REQUIRED NO_MODULE)
message(STATUS "Found Eigen3 ${Eigen3_VERSION}")

find_package(nlohmann_json REQUIRED)

add_subdirectory(${PROJECT_SOURCE_DIR}/../ext/bulk bulk)

find_package(Boost 1.61 COMPONENTS program_options REQUIRED)

add_library(astra-toolbox SHARED IMPORTED)
set_target_properties(
    astra-toolbox PROPERTIES
    IMPORTED_LOCATION ${CMAKE_PREFIX_PATH}/lib/libastra.so
    INTERFACE_COMPILE_DEFINITIONS "ASTRA_CUDA")
set(ASTRA_INCLUDE_DIR ${CMAKE_PREFIX_PATH}/include)

set(SOURCES
    "src/util/util.cpp"
    "src/util/bench.cpp"
    "src/reconstruction/projection_processor.cpp"
    "src/reconstruction/listener.cpp"
    "src/reconstruction/solver.cpp"
    "src/reconstruction/reconstructor.cpp"
    "src/reconstruction/helpers.cpp"
)
set(TARGET_NAME "_slicerecon")
add_library(${TARGET_NAME} ${SOURCES})
target_include_directories(${TARGET_NAME}
    PRIVATE
        ${ASTRA_INCLUDE_DIR}
    PUBLIC
        ${CMAKE_CURRENT_LIST_DIR}/include)
target_link_libraries(${TARGET_NAME}
    PUBLIC
        astra-toolbox
        tomopackets
        Eigen3::Eigen
        nlohmann_json::nlohmann_json
        spdlog::spdlog
        Boost::program_options
        bulk_thread
        ${FFTW_FLOAT_LIB}
)
target_compile_options(${TARGET_NAME}
    PRIVATE
        -std=c++17 -Wall -Wextra -Wfatal-errors -fPIC -static)

if (BUILD_PYTHON)
    set(BINDING_NAME "slicerecon")
    pybind11_add_module(${BINDING_NAME} "python/slicerecon.cpp")
    target_link_libraries(${BINDING_NAME} PRIVATE _slicerecon)

    install(TARGETS ${BINDING_NAME}
            LIBRARY DESTINATION ${Python3_SITELIB})
endif()

add_executable(tomcat-live-server "src/tomcat_live_server.cpp")
target_link_libraries(tomcat-live-server PRIVATE _slicerecon)

# INSTALL COMMANDS
install(TARGETS tomcat-live-server RUNTIME DESTINATION bin)
