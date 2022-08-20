for (let element of document.getElementsByClassName('header-user-nav-click')) {
    element.addEventListener('click', function () {
        let nav = document.getElementById('header-user-nav');
        let arrow = document.getElementById('header-user-arrow');
        let state = nav.style.opacity === '1';
        if (state) {
            nav.style.pointerEvents = 'none';
            nav.style.opacity = '0';
            nav.style.transform = 'scale(0.95)';
            arrow.style.transform = 'rotate(0deg)';
        } else {
            nav.style.pointerEvents = 'auto';
            nav.style.opacity = '1';
            nav.style.transform = 'scale(1)';
            arrow.style.transform = 'rotate(180deg)';
        }
    });
}

document.getElementById('mobile-nav-img').addEventListener('click', function() {
    let nav = document.getElementById('mobile-nav');
    let navImg = document.getElementById('mobile-nav-img');
    let state = nav.style.opacity === '1';
    if (state) {
        nav.style.pointerEvents = 'none';
        nav.style.opacity = '0';
        nav.style.transform = 'scale(0.95)';
        navImg.style.transform = 'rotate(0deg)';
    } else {
        nav.style.pointerEvents = 'auto';
        nav.style.opacity = '1';
        nav.style.transform = 'scale(1)';
        navImg.style.transform = 'rotate(-90deg)';
    }
});

let itemExitBtn = document.getElementById('item-exit');
if (itemExitBtn != null) {
    document.getElementById('item-exit').addEventListener('click', function() {
        fetch('api/v1/logout.php', {
            method: 'POST'
        }).then(async function (response) {
            location.reload();
        });
    });
}