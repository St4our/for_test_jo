import json

print(json.dumps({'Для зала': ['0', '131382.0'], 'None': ['235', '40'], 'Кальян': ['36', '10'], 'Не кальян': ['2161', '424'], 'авторские коктейли': ['3', '2'], 'Вок с курицей персонал': ['3', '0'], 'Паста с курицей персонал': ['5', '0'], 'Жульен с курицей персонал': ['1', '0'], 'Картофель Фри персонал': ['1', '0'], 'Суп с лапшой персонал': ['1', '0'], 'Кофе персонал': ['3', '0'], 'Пицца Маргарита 30см персонал': ['1', '0'], 'Поке с курицей персонал': ['5', '0'], 'Паста с грибами персонал': ['1', '0'], 'Курица карри': ['8', '2'], 'Митболы с картофельным пюре': ['2', '1'], 'Бифштекс из мраморной говядины с трюфельной заправкой': ['3', '1'], 'Курица по-азиатски': ['2', '0'], 'Карри 25см': ['3', '0'], 'Попкорн из креветок': ['3', '0'], 'Креветки темпура': ['9', '2'], 'Кола 0,25л': ['3', '0'], 'Кола Зеро 0,25л': ['10', '2'], 'Лук Фри': ['1', '0'], 'Феймос Грауз 40мл': ['1', '0'], 'Моти': ['18', '4'], 'Коко Липс': ['1', '1'], 'White Russian': ['1', '0'], 'Чай вишневый пуэр': ['13', '7'], 'Raspberry Spritz': ['3', '1'], 'Лимонад Арбуз-Базилик 900мл': ['16', '0'], 'Смузи киви яблоко мята': ['3', '0'], 'Смузи клубника-киви': ['11', '1'], 'Чай персик тимьян жасмин': ['10', '2'], 'Чай чёрная смородина-базилик': ['12', '4'], 'Шу-пуэр': ['1', '0'], 'Bramble': ['1', '1'], 'Саган Роуз': ['2', '1'], 'Молочно Ванильный': ['15', '3'], 'Молочно Шоколадный': ['11', '2'], 'Клубника Тимьян': ['9', '2'], 'Арахис Соленая карамель': ['4', '0'], 'Орео': ['13', '2'], 'Велада Рислинг': ['17', '0'], 'Велада Шардоне': ['2', '0'], 'Джин': ['1', '1'], 'Strawberry Rose': ['1', '1'], 'Латте Айс': ['4', '0'], 'Капучино Айс': ['1', '0'], 'Раф Айс': ['3', '0'], 'Зелёный + паровой коктейль': ['2', '2'], 'Фруктовый + паровой коктейль': ['5', '3'], 'Чёрный + паровой коктейль': ['4', '0'], 'Шото Тамань': ['2', '0'], 'Имбирный с лимоном и мёдом': ['7', '1'], 'Каркаде-грейпфрут': ['1', '0'], 'Малиновый мохито': ['21', '2'], 'Облепиховый с мёдом': ['8', '0'], 'Чай Пряный': ['1', '0'], 'Чай Цитрусовый': ['1', '0'], 'Aperol Spritz': ['2', '0'], 'Daiqiri': ['2', '0'], 'Strawberry Champantini': ['1', '0'], 'Long Island': ['4', '0'], 'Mai-Tai': ['2', '0'], 'Margarita': ['2', '0'], 'Martini Royal': ['2', '0'], 'Mojito': ['5', '0'], 'Pina Colada': ['2', '0'], 'Tequila Sunrise': ['1', '0'], 'Б/А Пина колада': ['10', '3'], 'Клубничный слинг': ['20', '5'], 'Манговый слинг': ['6', '1'], 'Молочно-шоколадный': ['3', '0'], 'Молочно-ванильный': ['4', '1'], 'Мохито': ['29', '11'], 'Мохито фруктовый': ['12', '3'], 'Шмель': ['19', '6'], 'Флюте': ['1', '0'], 'Вода "Бон Аква" газированная': ['1', '1'], 'Вода "Бон Аква" негазированная': ['5', '1'], 'Хаски 40мл': ['14', '8'], 'Лимон': ['4', '0'], 'Молоко': ['1', '0'], 'Мята': ['8', '2'], 'Чабрец': ['4', '3'], 'Контейнер': ['22', '1'], 'Крафт-Контейнер': ['2', '0'], 'Спрайт 1л': ['1', '1'], 'Акция Паровой коктейль': ['13', '6'], 'Паровой коктейль': ['23', '4'], 'Арарат 5* 40мл': ['1', '0'], 'Американо': ['5', '3'], 'Какао': ['4', '3'], 'Капучино': ['23', '4'], 'Альтернативное кокосовое молоко': ['2', '0'], 'Латте': ['14', '2'], 'Раф-кофе': ['14', '3'], 'Сироп': ['22', '5'], 'Эспрессо': ['1', '0'], 'Капучино c/c': ['4', '1'], 'Латте c/c': ['6', '3'], 'Раф-кофе c/c': ['1', '0'], 'Авторский "Лайм-лимон" 900 мл': ['3', '1'], 'Авторский лимонад "Дюшес" 900 мл': ['6', '0'], 'Вода с лимоном 1л': ['6', '1'], 'Вода с лимоном без газа': ['1', '1'], 'Лимонад "Ананас-кокос" 900мл': ['14', '2'], 'Лимонад "Апельсин-дыня" 900мл': ['22', '1'], 'Лимонад "Апельсин-манго-марак." 900мл': ['7', '3'], 'Лимонад "Вишнёвый" 900мл': ['1', '1'], 'Лимонад "Грейпфрут-клубника" 900мл': ['20', '3'], 'Лимонад "Яблоко-киви-мал" 900мл': ['6', '2'], 'Лимонад "Яблоко-Киви" 900мл': ['3', '0'], 'Лимонад "Ягодный" 900мл': ['23', '2'], 'Bergaer dark': ['15', '5'], 'Bergauer Blanche': ['24', '2'], 'Bergauer classic': ['42', '15'], 'Bergauer fest': ['26', '0'], 'Bergauer Pilsner': ['51', '12'], 'Demidov Б/А': ['14', '5'], 'Смузи клубника-банан': ['19', '3'], 'Смузи черная смородина': ['8', '2'], 'Сок "Rich" Ананас 0,25': ['1', '0'], 'Сок "Rich" Апельсин 0,25': ['7', '2'], 'Сок "Rich" Вишнёвый 0,25': ['6', '1'], 'Сок "Rich" Мультифрукт 0,25': ['1', '0'], 'Сок "Rich" Персиковый 0,25': ['2', '0'], 'Сок "Rich" Яблочный 0,25': ['14', '3'], 'Сок "Rich" Апельсин 1л': ['2', '0'], 'Спрайт 0.5л': ['2', '0'], 'Фреш апельсин': ['8', '0'], 'Фреш апельсин-яблоко': ['1', '1'], 'Фреш грейпфрут': ['3', '0'], 'Фреш морковь': ['1', '0'], 'Фреш яблоко': ['1', '1'], 'Фреш яблоко-морковь': ['2', '0'], 'Гречишный': ['4', '1'], 'Зелёный': ['6', '0'], 'Чёрный': ['8', '3'], 'Боска': ['2', '0'], 'Шамп. Российское': ['3', '0'], 'Burn 0.5л': ['2', '1'], 'Вок с креветкой': ['11', '1'], 'Вок с курицей': ['34', '6'], 'Вок с лососем': ['7', '0'], 'Вок с овощами и грибами': ['3', '1'], 'Бефстроганов с картофельным пюре': ['10', '2'], 'Жульен в булочке с грибами': ['5', '0'], 'Жульен в булочке с креветками': ['4', '0'], 'Жульен в булочке с курицей': ['14', '3'], 'Жульен в булочке с лососем': ['6', '0'], 'Овощи-гриль': ['2', '1'], 'Стейк из сёмги': ['2', '0'], 'Гренки бородинские': ['25', '4'], 'Картофель по-деревенски': ['3', '0'], 'Картофель фри': ['47', '5'], 'Креветки жареные': ['2', '0'], 'Куриные крылья чиз 4 шт': ['2', '1'], 'Луковые кольца': ['10', '1'], 'Пивной сет': ['2', '0'], 'Сырные палочки': ['1', '1'], 'Гор. Калифорния': ['11', '0'], 'Гор. Майами': ['11', '3'], 'Гор. Микс': ['2', '1'], 'Гор. Сэнсей': ['2', '0'], 'Гор. Филадельфия': ['1', '0'], 'Гор. Цезарь': ['8', '1'], 'Гор. Чикен': ['6', '2'], 'Грибы': ['4', '0'], 'Кокосовое молоко': ['1', '0'], 'Соус барбекю': ['13', '2'], 'Соус кисло-сладкий': ['6', '0'], 'Соус сырный': ['75', '16'], 'Соус Цезарь': ['3', '1'], 'Сырники из рикотты': ['1', '0'], 'Зап. с крабом и сливочным сыром': ['6', '1'], 'Зап. с креветкой и сливочным сыром': ['11', '2'], 'Зап. с курицей и сливочным сыром': ['13', '0'], 'Зап. с лососем': ['7', '1'], 'Зап. с угрём и сливочным сыром': ['4', '0'], 'Зап. батакон': ['3', '0'], 'Зап. калифорния': ['7', '0'], 'Зап. катана': ['1', '0'], 'Зап. микс': ['2', '2'], 'Зап. мульти': ['8', '2'], 'Зап. ричи': ['2', '0'], 'Зап. салмон': ['10', '1'], 'Зап. токати': ['5', '1'], 'Зап. филадельфия': ['9', '1'], 'Зап. эби': ['11', '2'], 'Кацу с креветками': ['9', '2'], 'Кацу с лососем': ['5', '1'], 'Кацу с цыпленком': ['17', '2'], 'С крабом и сливочным сыром': ['4', '2'], 'С креветкой и сливочным сыром': ['4', '2'], 'С лососем': ['5', '3'], 'С огурцом и сливочным сыром': ['11', '2'], 'С угрём': ['1', '0'], 'Чизкейк "Клубничный пломбир"': ['17', '2'], 'Чизкейк "Манго-маракуйя"': ['14', '5'], 'Чизкейк "Сникерс"': ['14', '0'], 'Остр. сафари': ['2', '0'], 'Остр. чикен': ['3', '0'], 'Остр. якитория': ['3', '1'], 'Остр. Якудза': ['3', '1'], 'Паста карбонара': ['18', '5'], 'Паста с грибами': ['10', '0'], 'Паста с креветками': ['25', '3'], 'Паста с курицей': ['20', '2'], 'Паста с лососем': ['11', '4'], 'Поке с креветкой': ['10', '0'], 'Поке с курицей': ['10', '2'], 'Поке с лососем': ['19', '2'], 'Греческий': ['11', '4'], 'Немецкий': ['28', '11'], 'Салат овощной с креветками-гриль': ['5', '2'], 'Салат с лососем шеф-посола': ['7', '0'], 'Тар-тар': ['25', '9'], 'Тёплый салат с курицей': ['10', '4'], 'Цезарь с креветками': ['14', '4'], 'Цезарь с курицей': ['46', '5'], 'Чука': ['4', '3'], 'Элегантный': ['11', '3'], 'Сет JOJO': ['10', '1'], 'Сет Классический': ['1', '0'], 'Сет МЕГА': ['6', '0'], 'Сет Микс': ['2', '0'], 'Сет Мини запечённый': ['6', '0'], 'Сет Премиум': ['9', '1'], 'Сет Селяви': ['2', '1'], 'Сет Удачный': ['2', '0'], 'Сет Филадельфия': ['1', '1'], 'Сет Хан': ['3', '1'], 'Крем-суп грибной': ['9', '2'], 'Куриный суп с лапшой': ['15', '3'], 'Сливочная уха по-царски': ['13', '5'], 'Суп сырный': ['7', '1'], 'Том ям+рис': ['52', '6'], 'Тостовый хлеб': ['18', '3'], 'Хлеб Бородинский': ['15', '6'], 'Сырная тарелка': ['1', '1'], 'Хол. ролл Дракон': ['3', '1'], 'Хол. ролл Зелёный дракон': ['5', '4'], 'Хол. ролл Калифорния': ['1', '0'], 'Хол. ролл Марфа': ['4', '1'], 'Хол. ролл Сливочный лайт': ['6', '1'], 'Хол. ролл Сырный': ['2', '0'], 'Хол. ролл Филадельфия': ['6', '4'], 'Ассорти': ['9', '1'], 'Жгучие биггер': ['1', '1'], 'Манго чили биггер': ['2', '0'], 'Медово горчичный биггер': ['3', '0'], 'Оранж барбекю биггер': ['2', '1'], 'Терияки-Имбирь биггер': ['1', '0'], 'Креветка-авокадо': ['4', '0'], 'Лосось-авокадо': ['6', '2'], 'Песто-вяленые томаты': ['2', '0'], 'Биф Карри': ['3', '0'], 'Двойной чизбургер': ['3', '1'], 'Джокович': ['13', '0'], 'Дорки-порки': ['11', '0'], 'Интеллигент': ['3', '0'], 'Итальянский': ['9', '3'], 'Мудрый егерь': ['3', '0'], 'С ума сойти': ['8', '1'], 'Самбрерро': ['2', '0'], 'Сытый внук': ['18', '3'], 'Чизбургер': ['44', '6'], 'Чикен карри': ['1', '0'], 'Шахтер': ['21', '6'], 'Стрипсы 4шт': ['1', '0'], 'Стрипсы 8шт': ['2', '0'], 'Нагетсы 12шт': ['7', '1'], 'Нагетсы 8шт': ['27', '4'], 'По-деревенски': ['18', '7'], 'Фри': ['48', '13'], 'Жгучие стандарт': ['4', '1'], 'Манго чили стандарт': ['1', '0'], 'Медово-горчичный стандарт': ['9', '2'], 'Оранж-барбекю стандарт': ['11', '2'], 'Терияки-имбирь стандарт': ['1', '0'], 'Томатная классика стандарт': ['1', '1'], 'Сэндвич с курицей': ['3', '0'], 'Фри с реберным мясом': ['42', '8'], '4 сыра 25см': ['6', '1'], 'Гавайи 25см': ['3', '1'], 'Грибная 25см': ['1', '0'], 'Домашняя 25см': ['7', '2'], 'Пепперони 25см': ['11', '2'], '4 сыра 30см': ['7', '2'], 'Гавайи 30см': ['6', '1'], 'Грибная 30см': ['2', '1'], 'Домашняя 30см': ['8', '1'], 'Маргарита 30см': ['1', '0'], 'Острая 30см': ['2', '0'], 'Пепперони 30см': ['10', '1'], 'Бушмилс 40мл': ['1', '1'], 'Глинтвейн': ['1', '1'], 'С авокадо и сливочным сыром': ['1', '1']}))