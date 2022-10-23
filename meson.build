project('luniversalinstaller',
          version: '0.2',
    meson_version: '>= 0.59.0',
  default_options: [ 'warning_level=2', 'werror=false', ],
)


data_files = [
              ['applications', ['com.github.yucefsourani.LUniversalInstaller.desktop']],
              ['doc/luniversalinstaller', ['LICENSE',  'README.md']],
              ['icons/hicolor/16x16/apps', ['hicolor/16x16/apps/com.github.yucefsourani.LUniversalInstaller.png']],
              ['icons/hicolor/22x22/apps', ['hicolor/22x22/apps/com.github.yucefsourani.LUniversalInstaller.png']],
              ['icons/hicolor/24x24/apps', ['hicolor/24x24/apps/com.github.yucefsourani.LUniversalInstaller.png']],
              ['icons/hicolor/32x32/apps', ['hicolor/32x32/apps/com.github.yucefsourani.LUniversalInstaller.png']],
              ['icons/hicolor/36x36/apps', ['hicolor/36x36/apps/com.github.yucefsourani.LUniversalInstaller.png']],
              ['icons/hicolor/48x48/apps', ['hicolor/48x48/apps/com.github.yucefsourani.LUniversalInstaller.png']],
              ['icons/hicolor/64x64/apps', ['hicolor/64x64/apps/com.github.yucefsourani.LUniversalInstaller.png']],
              ['icons/hicolor/72x72/apps', ['hicolor/72x72/apps/com.github.yucefsourani.LUniversalInstaller.png']],
              ['icons/hicolor/96x96/apps', ['hicolor/96x96/apps/com.github.yucefsourani.LUniversalInstaller.png']],
              ['icons/hicolor/128x128/apps',['hicolor/128x128/apps/com.github.yucefsourani.LUniversalInstaller.png']],
              ['pixmaps',['hicolor/128x128/apps/com.github.yucefsourani.LUniversalInstaller.png']]
              ]
              
data_folders = [
                 ['luniversalinstaller', ['plugins']],
                 ['luniversalinstaller/plugins', ['plugins/universalplugin']],
                 ['luniversalinstaller', ['images']]
               ]
foreach files_ : data_files
  foreach i : files_[1]
    install_data(
      i,
      install_dir : join_paths(get_option('datadir'),files_[0])
  )
  endforeach
endforeach

foreach folder_ : data_folders
  foreach i : folder_[1]
    install_subdir(
      i,
      install_dir : join_paths(get_option('datadir'),folder_[0])
  )
  endforeach
endforeach

install_data(
    'luniversalinstaller.py',
    install_dir : get_option('bindir')
)

desktop_utils = find_program('desktop-file-validate', required: false)
if desktop_utils.found()
  test('Validate desktop file', desktop_utils, args: [join_paths(get_option('datadir'), 'applications','com.github.yucefsourani.LUniversalInstaller.desktop')])
endif

