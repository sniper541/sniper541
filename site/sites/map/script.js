// Инициализация карты
const map = L.map('map', {
    minZoom: 2,
    maxBounds: [[-90, -180], [90, 180]],
    maxBoundsViscosity: 1.0
}).setView([20, 0], 2);

console.log('Карта инициализирована');

// Темы карты
const baseLayers = {
    'Стандартная': L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
        maxZoom: 15
    }),
    'Тёмная': L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
        attribution: '© <a href="https://carto.com/attributions">CARTO</a>, © <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
        maxZoom: 15
    }),
    'Спутниковая': L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
        attribution: 'Tiles © Esri — Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community',
        maxZoom: 15
    })
};
// Устанавливаем стандартную карту по умолчанию
baseLayers['Стандартная'].addTo(map);
L.control.layers(baseLayers).addTo(map);

console.log('Слой карты добавлен (Стандартная по умолчанию)');

// Хранилище данных о местах
let visitedPlaces = [];
let editPassword = null;

// Загрузка данных с сервера
async function loadCitiesFromDB() {
    console.log('Отправка запроса на /map/get_places');
    try {
        const response = await fetch('/map/get_places');
        console.log('Ответ от /map/get_places:', response.status, response.statusText);
        if (response.ok) {
            visitedPlaces = await response.json();
            console.log('Загружено с сервера:', visitedPlaces);
            visitedPlaces.forEach(place => {
                if (place.latitude && place.longitude) {
                    addMarker([place.latitude, place.longitude], place.name);
                }
            });
        } else {
            console.error('Ошибка загрузки с сервера:', response.status, response.statusText);
            const errorText = await response.text();
            console.error('Текст ошибки:', errorText);
        }
    } catch (error) {
        console.error('Ошибка загрузки с сервера:', error);
    }
}

// Сохранение данных на сервер
async function saveToDB() {
    if (!editPassword) {
        console.error('Пароль для редактирования не установлен');
        return;
    }

    console.log('Отправка запроса на /map/save_places с данными:', visitedPlaces);
    console.log('Пароль:', editPassword);
    try {
        const response = await fetch('/map/save_places', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-Edit-Password': editPassword
            },
            body: JSON.stringify(visitedPlaces)
        });
        console.log('Ответ от /map/save_places:', response.status, response.statusText);
        if (response.ok) {
            const result = await response.json();
            console.log('Данные успешно сохранены на сервере:', result);
        } else {
            console.error('Ошибка сохранения на сервера:', response.status, response.statusText);
            const errorText = await response.text();
            console.error('Текст ошибки:', errorText);
        }
    } catch (error) {
        console.error('Ошибка сохранения на сервере:', error);
    }
}

// Функция обратного геокодирования с Nominatim API (на русском)
async function reverseGeocode(lat, lng) {
    try {
        const response = await fetch(
            `https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lng}&zoom=10&addressdetails=1&accept-language=ru`,
            {
                headers: {
                    'User-Agent': 'TravelMapApp/1.0 (your-email@example.com)' // Замените на ваш email
                }
            }
        );
        const data = await response.json();
        if (data && data.address) {
            const city = data.address.city || data.address.town || data.address.village || data.address.hamlet || 'Неизвестное место';
            return city;
        }
        return `Место (${lat.toFixed(2)}, ${lng.toFixed(2)})`;
    } catch (error) {
        console.error('Ошибка геокодирования:', error);
        return `Место (${lat.toFixed(2)}, ${lng.toFixed(2)})`;
    }
}

// Слой для маркеров
let markersLayer = L.layerGroup().addTo(map);
let editMode = false;

// Кастомная иконка (иголка)
const pinIcon = L.icon({
    iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
    shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    shadowSize: [41, 41],
    shadowAnchor: [12, 41],
    popupAnchor: [1, -34]
});

// Функция добавления маркера
function addMarker(latlng, name) {
    const marker = L.marker(latlng, {
        draggable: editMode,
        icon: pinIcon
    }).addTo(markersLayer);

    marker.bindPopup(name || `Место (${latlng.lat.toFixed(2)}, ${latlng.lng.toFixed(2)})`);

    let clickCount = 0;
    let clickTimer = null;

    marker.on('click', function(e) {
        if (!editMode) return;

        clickCount++;
        if (clickCount === 1) {
            clickTimer = setTimeout(() => {
                console.log(`Клик по месту: ${name || marker.getPopup().getContent()}`);
                clickCount = 0;
            }, 300);
        }
    });

    marker.on('dblclick', function(e) {
        if (!editMode) return;

        clearTimeout(clickTimer);
        clickCount = 0;

        if (confirm(`Удалить метку "${name || marker.getPopup().getContent()}"?`)) {
            const index = visitedPlaces.findIndex(p => p.name === (name || marker.getPopup().getContent()));
            if (index !== -1) {
                visitedPlaces.splice(index, 1);
                markersLayer.removeLayer(marker);
                saveToDB();
                console.log(`Метка "${name || marker.getPopup().getContent()}" удалена`);
            }
        }
    });

    if (editMode) {
        marker.on('dragend', function(e) {
            const newLatLng = e.target.getLatLng();
            const popupContent = marker.getPopup().getContent();
            const place = visitedPlaces.find(p => p.name === popupContent);
            if (place) {
                place.latitude = newLatLng.lat;
                place.longitude = newLatLng.lng;
            }
            markersLayer.removeLayer(marker);
            addMarker(newLatLng, popupContent);
            saveToDB();
        });
    }
}

// Переключатель режима редактирования
document.addEventListener('DOMContentLoaded', function() {
    const editToggle = document.getElementById('edit-mode-toggle');
    const controls = document.getElementById('controls');
    if (!editToggle || !controls) {
        console.error('Элемент edit-mode-toggle или controls не найден');
    } else {
        console.log('Переключатель найден');
        editToggle.addEventListener('change', function() {
            if (this.checked) {
                const password = prompt("Введите пароль для режима редактирования:");
                if (password === "masters") {
                    editMode = true;
                    editPassword = password; // Сохраняем пароль для отправки на сервер
                    controls.classList.add('edit-mode');
                    alert("Режим редактирования включен! Щелкните правой кнопкой, чтобы добавить метку. Двойной клик для удаления.");
                    markersLayer.eachLayer(layer => layer.dragging.enable());
                } else {
                    this.checked = false;
                    alert("Неверный пароль!");
                }
            } else {
                editMode = false;
                editPassword = null;
                controls.classList.remove('edit-mode');
                alert("Режим редактирования выключен!");
                markersLayer.eachLayer(layer => layer.dragging.disable());
            }
        });
    }

    // Загружаем данные при запуске
    loadCitiesFromDB();
});

// Поиск местоположений (на русском)
document.getElementById('search').addEventListener('input', async function() {
    const query = this.value;
    if (query.length < 3) return; // Минимальная длина запроса
    try {
        const response = await fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(query)}&accept-language=ru`, {
            headers: { 'User-Agent': 'TravelMapApp/1.0 (your-email@example.com)' } // Замените на ваш email
        });
        const data = await response.json();
        if (data[0]) {
            map.setView([data[0].lat, data[0].lon], 10);
        }
    } catch (error) {
        console.error('Ошибка поиска:', error);
    }
});

// Добавление нового маркера по правому клику
map.on('contextmenu', async function(e) {
    if (editMode) {
        const latlng = e.latlng;
        const defaultCityName = await reverseGeocode(latlng.lat, latlng.lng);
        const name = prompt('Введите название места:', defaultCityName);
        if (name) {
            addMarker(latlng, name);
            visitedPlaces.push({ name, latitude: latlng.lat, longitude: latlng.lng });
            saveToDB();
        }
    }
});