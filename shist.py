import curses
import os

def search_commands(history, query):
    matching_commands = []
    if query is not "":
        for cmd in history:
            if query in cmd:
                matching_commands.append(cmd)
    return matching_commands


def main(stdscr):

    history = open(os.path.expanduser("~/.zsh_history"), "r").readlines()

    # curses.curs_set(0)
    stdscr.clear()
    curses.start_color()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(5, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    search_query = ""
    selection = 0
    scroll_position = 0
    selected_cmd = None
    
    while True:
        stdscr.clear()

        matching_commands = search_commands(history, search_query)
        matching_commands.reverse()
        num_results = len(matching_commands)
        num_displayable = min(num_results, curses.LINES - 1)

        if num_results == 0 or not search_query:
            stdscr.addstr(curses.LINES - 2, 0, "No matches found!", curses.color_pair(1))
        else:
            stdscr.addstr(curses.LINES - 2, 0, "  %s/%s"%(selection + 1, num_results), curses.color_pair(5) | curses.A_DIM)
            for i in range(num_displayable):
                row = curses.LINES - 3 - i
                if 0 <= row < curses.LINES:
                    if i == selection:
                        stdscr.addstr(row, 0, "> " + matching_commands[i + scroll_position], curses.color_pair(4))
                        stdscr.addstr(row, 2, matching_commands[i + scroll_position], curses.color_pair(4))
                    else:
                        stdscr.addstr(row, 0, " ", curses.color_pair(4))
                        stdscr.addstr(row, 1, " ", curses.color_pair(3))
                        stdscr.addstr(row, 2, matching_commands[i + scroll_position], curses.color_pair(3) | curses.A_DIM)

        stdscr.addstr(curses.LINES - 1, 0, "Search History: ", curses.color_pair(2) | curses.A_BOLD)
        stdscr.addstr(curses.LINES - 1, len("Search History: "), search_query, curses.color_pair(3))
        stdscr.move(curses.LINES - 1, len("Search History: " + search_query))

        stdscr.refresh()

        key = stdscr.getch()
        if key == 27:  # ESC key
            break
        elif key == 10:  # Enter key
            if 0 <= selection < num_results:
                selected_cmd = matching_commands[selection + scroll_position].strip()
                break
        elif key == curses.KEY_DOWN:
            selection = max(selection - 1, 0)
            if selection == 0 and scroll_position > 0:
                scroll_position -= 1
        elif key == curses.KEY_UP:
            selection = min(selection + 1, num_displayable - 1)
            if selection == num_displayable - 1 and scroll_position < num_results - num_displayable:
                scroll_position += 1
        elif key >= 32 and key <= 126: # user is typing
            search_query += chr(key)
            selection = 0
            scroll_position = 0
        elif key == curses.KEY_BACKSPACE or key == 127:  # Backspace key
            search_query = search_query[:-1]
            selection = 0
            scroll_position = 0

    if selected_cmd != None:
        print("cmd: %s"%(selected_cmd))

if __name__ == "__main__":
    curses.wrapper(main)
