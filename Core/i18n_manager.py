import builtins
import gettext
import os
import wx
from Core.JSON_load import default_user_db_path


def get_setting_language():
    """从配置文件中读取语言设置，若失败返回 None"""
    try:
        default_url_file = default_user_db_path(r"Bin/Config/Default/default_address.json")
        return default_url_file["setting"]["language"]
    except Exception:
        return None


class I18nManager:
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        # domain 固定为 en，因为 .mo 文件名为 en.mo
        self.domain = 'en'

        self.locale_dir = "./Data/locale"
        
        self.translation = None
        self.current_language = None
        
        # 初始化时检查并修复目录结构
        self._ensure_locale_structure()

    def _ensure_locale_structure(self):
        """确保翻译文件目录结构正确"""
        try:
            import shutil
            
            # 定义所有支持的语言及其源文件位置
            languages_config = {
                'zh_CN': {
                    'source_mo': None,  # 中文是默认语言，如果没有翻译文件就使用原文
                    'needs_creation': True
                },
                'en': {
                    'source_mo': os.path.join(self.locale_dir, "en", "LC_MESSAGES", "en.mo"),
                    'needs_creation': False  # en目录已存在
                },
                'ja_JP': {
                    'source_mo': os.path.join(self.locale_dir, "ja_JP", "LC_MESSAGES", "ja_JP.mo"),
                    'wrong_name': os.path.join(self.locale_dir, "ja_JP", "LC_MESSAGES", "ja_JP.mo"),
                    'correct_name': os.path.join(self.locale_dir, "ja_JP", "LC_MESSAGES", "en.mo"),
                    'needs_creation': False
                },
                'zh_TW': {
                    'source_mo': os.path.join(self.locale_dir, "zh_TW", "LC_MESSAGES", "zh_TW.mo"),
                    'wrong_name': os.path.join(self.locale_dir, "zh_TW", "LC_MESSAGES", "zh_TW.mo"),
                    'correct_name': os.path.join(self.locale_dir, "zh_TW", "LC_MESSAGES", "en.mo"),
                    'needs_creation': False
                }
            }
            
            # 处理每个语言
            for lang, config in languages_config.items():
                lang_dir = os.path.join(self.locale_dir, lang, "LC_MESSAGES")
                target_mo = os.path.join(lang_dir, "en.mo")
                
                os.makedirs(lang_dir, exist_ok=True)
                
                if lang in ['ja_JP', 'zh_TW']:
                    wrong_path = config.get('wrong_name')
                    if wrong_path and os.path.exists(wrong_path) and not os.path.exists(target_mo):
                        shutil.move(wrong_path, target_mo)

                # 对于中文，如果没有翻译文件，创建一个空的.mo文件（使用fallback）
                if lang == 'zh_CN' and not os.path.exists(target_mo):
                    print(f"ℹ 中文使用默认文本（无需翻译文件）")
                        
        except Exception as e:
            print(f"⚠ 检查翻译目录结构时出错: {e}")

    def install_placeholder(self):
        """
        安装一个临时的 _ 函数，防止因翻译未加载而报错
        :return:
        """
        if not hasattr(builtins, '_'):
            builtins._ = lambda x: x

    def init_translation(self, language=None):
        """
        加载翻译并安装到 builtins._
        :param language: 目标语言，如 'zh_CN' 或 'en'；若为 None 则使用 self.current_language
        """
        if language:
            self.current_language = language
        elif self.current_language is None:
            # 从未设置过语言，默认中文
            self.current_language = 'zh_CN'

        try:
            self.translation = gettext.translation(
                self.domain,
                localedir=self.locale_dir,
                languages=[self.current_language],
                fallback=True
            )
            self.translation.install()

            return True

        except Exception as e:

            # 确保 _ 函数至少可用（回退到原样返回）
            if not hasattr(builtins, '_'):
                builtins._ = lambda x: x
            return False

    def fix_wx_locale_override(self):
        """
        wx.Locale 初始化后可能会覆盖 builtins._，需要重新安装
        :return:
        """
        try:
            # 尝试创建 wx.Locale（如果尚未创建）
            locale = wx.Locale()
            try:
                locale.Init(wx.LANGUAGE_DEFAULT)
            except:
                pass
        except:
            pass

        # 重新安装 gettext 翻译
        if self.translation:
            self.translation.install()
        else:
            # 如果之前加载失败，再次尝试（使用当前语言）
            self.init_translation()

    @classmethod
    def initialize(cls, language=None):
        """
        一站式初始化入口。
        :param language: 可选，强制指定语言。若不指定，则从配置文件读取。
                         若配置文件无效或语言不支持，默认使用 'zh_CN'（中文）
        """
        manager = cls()
        manager.install_placeholder()

        if language is None:
            config_lang = get_setting_language()
            # 支持的语言列表：zh_CN(中文), en(英文), ja_JP(日文), zh_TW(繁体)
            supported_languages = ('zh_CN', 'en', 'ja_JP', 'zh_TW')
            if config_lang not in supported_languages:
                config_lang = 'zh_CN'  # 默认中文
            language = config_lang

        manager.init_translation(language)
        # 注意：fix_wx_locale_override() 需要在 wx.App 创建后调用
        return manager

    def set_language(self, language):
        """
        切换当前语言并重新加载翻译
        :param language:
        :return:
        """
        if self.current_language == language:
            return
        self.current_language = language
        self.init_translation(language)
        try:
            if wx.GetApp() is not None:
                self.fix_wx_locale_override()
        except:
            pass
