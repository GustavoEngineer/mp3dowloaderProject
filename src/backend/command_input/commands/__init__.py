from .help_command import HelpCommand
from .wifi_command import WifiCommand
from .clear_command import ClearCommand
from .exit_command import ExitCommand
from .nav_command import NavCommand
from .create_command import CreateCommand
from .edit_command import EditCommand
from .delete_command import DeleteCommand
from .back_command import BackCommand
from .export_command import ExportCommand

# Mapa centralizado de comandos modulares (fácil de extender)
COMMAND_MAP = {
    "help": HelpCommand(),
    "wifi": WifiCommand(),
    "clear": ClearCommand(),
    "exit": ExitCommand(),
    "nav": NavCommand(),
    "create": CreateCommand(),
    "edit": EditCommand(),
    "delete": DeleteCommand(),
    "rm": DeleteCommand(),
    "back": BackCommand(),
    "export": ExportCommand()
}
