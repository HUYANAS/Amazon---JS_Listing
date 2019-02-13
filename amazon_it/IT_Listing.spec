# -*- mode: python -*-

block_cipher = pyi_crypto.PyiBlockCipher(key='HY950407')


a = Analysis(['IT_Listing.py'],
             pathex=['D:\\ÏîÄ¿01\\program01\\amazon_it'],
             binaries=[],
             datas=[],
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
          name='IT_Listing',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True , icon='amazon_128px_1171929_easyicon.net.ico')
