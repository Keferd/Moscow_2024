
function getColorFromGradient(value) {
    // Преобразуем значение от 0 до 100 в диапазон от 0 до 1
    var normalizedValue = value / 100;

    // Создаем градиент
    var ctx = document.createElement("canvas").getContext("2d");
    var gradient = ctx.createLinearGradient(0, 0, 100, 0);

    // Добавляем цветовые остановки
    gradient.addColorStop(0, "red");    // Цвет на 0%
    gradient.addColorStop(0.5, "orange");    
    gradient.addColorStop(0.8, "green"); 
    gradient.addColorStop(1, "green");     // Цвет на 100%

    // Получаем цвет для заданного значения
    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, 100, 1);  // Рисуем градиент по одной строке высотой
    var color = ctx.getImageData(normalizedValue * 100, 0, 1, 1).data;

    // Преобразуем значения RGBA в строку hex
    var hexColor = "#" + ("000000" + ((color[0] << 16) | (color[1] << 8) | color[2]).toString(16)).slice(-6);

    return hexColor;
}








function changeSorting(sorting, courses) {


    const coursesArray = Object.values(courses);
    const new_courses = {};

    switch (sorting) {
        case 'relevant':
            coursesArray.sort((a, b) => parseInt(a.accuracy) - parseInt(b.accuracy));

            coursesArray.reverse();

            coursesArray.forEach(function(item, key, coursesArray) {
                new_courses[key] = item
            });

            break;
        case 'cheap':
            coursesArray.sort((a, b) => parseInt(a.price) - parseInt(b.price));

            // coursesArray.reverse();

            coursesArray.forEach(function(item, key, coursesArray) {
                new_courses[key] = item
            });

            break;
        case 'expensive':
            coursesArray.sort((a, b) => parseInt(a.price) - parseInt(b.price));

            coursesArray.reverse();

            coursesArray.forEach(function(item, key, coursesArray) {
                new_courses[key] = item
            });

            break;    
        default:
          alert( "changeSorting ERROR" );
      }

    return new_courses
}













let sendfilebtn = document.getElementById("send_link_btn");

sendfilebtn.addEventListener("click", function (e) {
    e.preventDefault();
    
    link_vacancy = document.getElementById("link_vacancy").value
    let formdata = JSON.stringify({link_vacancy: link_vacancy});

    if (typeof link_vacancy != 'undefined') {
        document.getElementById("main__result-container").innerHTML = `
            <div class="img__container">
                <img class="img__loading" src="static/img/loading.png" alt="loading">
            </div>

            <style>
                .img__container {
                    flex: 1;
                    width: 100%;
                    height: 100%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                }

                .img__loading {
                    width: 100px;
                    height: 100px;
                    animation: rotate_img 0.5s linear infinite;
                }

                @keyframes rotate_img {
                    0% {
                      transform: rotate(0deg);
                    }
                    100% {
                      transform: rotate(360deg);
                    }
                  }
            </style>
        `;
        

        fetch("/api/link",
        {
            method: "POST",
            body: formdata,
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then( response => {
            response.json().then(function(data) {

                console.log(data.skills);
                console.log(data.courses);

                let courses = data.courses 

                console.log(courses)

                // ------------------------------ СБОРКА HTML ВЫВОДА ----------------------------------------

                let newhtml = ``

                newhtml +=  `
                <div class="main__required-skills__container main__container">
                    <div class="main__title">
                        Необходимые навыки:
                    </div>
                    <div class="main__required-skills__list">
                `;

                for (i in data.skills){
                    newhtml +=  `<div>` + data.skills[i] + `</div>`
                }

                newhtml +=  `
                    </div>
                </div>
                <div class="main__search-overlay">
                    <div class="main__search-overlay__title" id="main__search-overlay__title">
                        
                    </div>
                    <div>
                        <select class="main__search-overlay__select" id="main__search-overlay__select">
                            <option value='relevant' selected>Сначала подходящие</option>
                            <option value='cheap'>Сначала дешевле</option>
                            <option value='expensive'>Сначала дороже</option>
                        </select>
                    </div>
                </div>
                `;

                newhtml += `
                <div class="main__list-of-courses" id="main__list-of-courses">
                </div>
                `;

                // ------------------------------ ЗАВЕРШЕНИЕ СБОРКИ HTML ВЫВОДА ----------------------------------------

                document.getElementById("main__result-container").innerHTML = newhtml
            
                courses = changeSorting(document.getElementById("main__search-overlay__select").value, courses)

                function constructionListOfCourses(courses) {
                    let newListOfCourseshtml = ``

                    for (i in courses){
                        let duration = ``
                        if (courses[i].duration){
                            duration = `<div>Срок обучения: ` + courses[i].duration + ` месяцев</div>`;
                        }

                        newListOfCourseshtml +=  `
                            <div class="main__container main__list-of-courses__container">
                                <div class="main__list-of-courses__left">
                                    <div>
                                        <a class="main__list-of-courses__left__title" target="_blank" href="` + courses[i].link + `">` + courses[i].name + `</a>
                                        <div class="main__list-of-courses__left__description">
                                        ` + courses[i].description + `
                                        </div>
                                        <div class="main__list-of-courses__left__partition"></div>
                                        `+ duration + `
                                    </div>
                                    <div class="main__list-of-courses__left__price">от ` + courses[i].price + `₽ в месяц</div>
                                </div>
                                <div class="main__list-of-courses__partition"></div>
                                <div class="main__list-of-courses__right">
                                    <div class="main__list-of-courses__right__title">
                                        Подходит на: <span style="color: ` + getColorFromGradient(courses[i].accuracy) + `">` + courses[i].accuracy + `</span>
                                    </div>
                                    <div class="main__list-of-courses__right__partition"></div>
                                    <div class="main__list-of-courses__right__subtitle">Совпадение по навыкам:</div>
                                    <div>
                                        <div class="main__list-of-courses__right__list">
                        `;
    
                        for (j in courses[i].skills){
                            newListOfCourseshtml +=  `<div>` + courses[i].skills[j] + `</div>`
                        };
    
                        newListOfCourseshtml += `
                                        </div>  
                                    </div>
                                </div>
                            </div>
                        `;
                    }

                    document.getElementById("main__list-of-courses").innerHTML = newListOfCourseshtml
                };

                

                function changeFormats(courses) {

                    let checkboxes = document.getElementById("main__filters__form");
                    var checkedLabels = [];
                    for (var i = 0; i < checkboxes.length; i++) {
                        if (checkboxes[i].checked) {
                            var label = document.querySelector('label[for="' + checkboxes[i].id + '"]');
                            checkedLabels.push(label.textContent);
                        }
                    }

                    console.log(checkedLabels);

                    let new_courses_filtered = {}

                    for (var courseId in courses) {
                        var course = courses[courseId];
                        var formats = Object.values(course.formats);
                        var containsAllLabels = checkedLabels.every(function(label) {
                            return formats.includes(label);
                        });
                        
                        // Если все метки присутствуют, добавить курс в новый объект
                        if (containsAllLabels) {
                            new_courses_filtered[courseId] = course;
                        }
                    }

                    // Вывод результата
                    console.log(new_courses_filtered);

                    return new_courses_filtered;
                }

                function changePrice(courses) {

                    let minVal = parseInt($("#minAmount").val());
                    let maxVal = parseInt($("#maxAmount").val());


                    let new_courses_filtered = {}

                    for (var courseId in courses) {
                        if (minVal <= Number(courses[courseId].price) && Number(courses[courseId].price) <= maxVal) {
                            console.log(minVal, courses[courseId].price, maxVal)
                            new_courses_filtered[courseId] = courses[courseId];
                        }
                    }

                    // Вывод результата
                    console.log(new_courses_filtered);

                    return new_courses_filtered;
                }

                function callchange() {
                    // Отфильтировать список курсов на текущее состояние 
                    filtered_courses = changeSorting(document.getElementById("main__search-overlay__select").value, changeFormats(changePrice(courses)));
                    
                    // Если состав курсов изменился - загрузить новую страницу
                    if (filtered_courses != courses){
                        constructionListOfCourses(filtered_courses);

                        document.getElementById("main__search-overlay__title").innerHTML = `Подходящие вакансии ` + Object.keys(filtered_courses).length + `:`;
                    }
                }


                filtered_courses = changeSorting(document.getElementById("main__search-overlay__select").value, changeFormats(changePrice(courses)));
                constructionListOfCourses(filtered_courses);
                document.getElementById("main__search-overlay__title").innerHTML = `Подходящие вакансии ` + Object.keys(changeFormats(filtered_courses)).length + `:`;

                document.getElementById("main__search-overlay__select").addEventListener("change", function() {
                    // courses = changeSorting(document.getElementById("main__search-overlay__select").value, courses)
                    // constructionListOfCourses(courses);
                    callchange()
                });


                document.getElementById("main__filters__form").addEventListener("change", function() {
                    callchange()
                });

                mouseDownInside = false;
                document.getElementById("slider-range").addEventListener('mousedown', function() {
                    mouseDownInside = true;
                });

                document.addEventListener('mouseup', function() {
                    if (mouseDownInside) {
                        callchange()
                    }
                    mouseDownInside = false;
                });

                // document.getElementById("slider-range").addEventListener('mouseleave', function() {
                //     callchange()
                // });

                // document.getElementById("slider-range").addEventListener('mouseup', function() {
                //     callchange()
                // });

                $("#minAmount, #maxAmount").change(function() {
                    callchange()
                });

            });
        })
        .catch( error => {
            alert(error);
            console.error('error:', error);
        });
        
    }
    else {
        // document.getElementById("error").innerHTML = `
        //     <div style="color: red;">
        //         Выберите файл
        //     </div>
        // `
    }
});