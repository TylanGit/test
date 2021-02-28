# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['client.py'],
             pathex=['C:\\Users\\PC\\Desktop\\Folder\\Computer Science\\Projects\\Shooty Arena'],
             binaries=[],
             datas=[('backgrounds/*','backgrounds/'),('blocks/*','blocks/'),('buttons/*','buttons/'),('fonts/*','fonts/'),('leveldata/*','leveldata/'),('players/*','players/')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='client',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False )
