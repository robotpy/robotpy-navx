project('robotpy-navx', ['cpp'],
        default_options: ['warning_level=1', 'cpp_std=c++20',
                          'b_colorout=auto', 'optimization=2', 'b_pie=true'])

subdir('semiwrap')

navx_sources += files(
    'navx/src/rpy/navx.cpp',
)

#
# Static link
#

cpp = meson.get_compiler('cpp')
libs_path = meson.current_source_dir() + '/lib/lib'

navx_deps += [
    cpp.find_library('StudicaDriver', dirs: libs_path),
    cpp.find_library('StudicaLibDriver', dirs: libs_path),
    cpp.find_library('Studica', dirs: libs_path),
    cpp.find_library('StudicaLib', dirs: libs_path),
]

subdir('semiwrap/modules')
