// $(document).ready(function () {
//     setTimeout(function () {
//         $('.alert').fadeOut('slow');
//     }, 2000)
// });
//

const _location = document.location.pathname;
let navBars = document.getElementsByClassName('btn btn-success m-1');
for (let nav in navBars){
    if (navBars[nav].href.includes( _location)){
        console.log(navBars[nav].href.includes( _location));
        navBars[nav].classList.add('btn-warning');
        break;
    }
}
