<?php
session_start();

// Путь к файлу с данными пользователей
$userDataFile = __DIR__ . '/json/login.json';

// Проверка существования файла
if (!file_exists($userDataFile)) {
    // Создание файла с пустым массивом пользователей
    file_put_contents($userDataFile, json_encode([]));
}

// Чтение и декодирование данных пользователей
$users = json_decode(file_get_contents($userDataFile), true);

// Проверка успешности декодирования
if (!is_array($users)) {
    $users = [];
}

// Инициализация переменных
$username = '';
$password = '';
$error = '';

// Обработка отправки формы
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $username = $_POST['username'] ?? '';
    $password = $_POST['password'] ?? '';

    // Проверка введенных данных
    $authenticated = false;
    foreach ($users as $user) {
        if ($user['username'] === $username && $user['password'] === $password) {
            $authenticated = true;
            break;
        }
    }

    if ($authenticated) {
        $_SESSION['username'] = $username;
        header('Location: owner.html');
        exit();
    } else {
        $error = 'Неверный логин или пароль!';
    }
}
?>
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Авторизация</title>
    <link rel="stylesheet" href="css/login.css">
</head>
<body class="dark-theme">
    <div class="login-container">
        <?php if ($error): ?>
            <div class="error-message"><?php echo htmlspecialchars($error); ?></div>
        <?php endif; ?>
        <form action="login.php" method="POST">
            <input type="text" name="username" placeholder="Логин" value="<?php echo htmlspecialchars($username); ?>" required>
            <input type="password" name="password" placeholder="Пароль" required>
            <button type="submit">Войти</button>
        </form>
    </div>
    <div class="theme-toggle">
        <label class="switch">
            <input type="checkbox" id="theme-switch">
            <span class="slider"></span>
        </label>
    </div>
    <script src="js/theme-toggle.js"></script>
</body>
</html>
