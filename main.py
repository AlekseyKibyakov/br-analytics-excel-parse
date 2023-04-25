import get_excel_file as get_xlsx
import schedule
import parsing_excel as parse_xlsx


def main():
    schedule.every().day.at('12:28').do(get_xlsx.run)
    schedule.every().day.at('12:29').do(parse_xlsx.run)
    

if __name__ == '__main__':
    main()
