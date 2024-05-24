const title = document.querySelector('.title')
const bush2 = document.querySelector('.bush2')
const mountain1 = document.querySelector('.mountain1')
const mountain2 = document.querySelector('.mountain2')
const main_logo = document.querySelector('.main_logo')

document.addEventListener('scroll', function() {
    let value = window.scrollY
    // console.log(value)
    title.style.marginTop = value * 0.5 + 'px'
    bush2.style.marginBottom = -value * 0.8 + 'px'
    mountain1.style.marginBottom = -value * 1.1 + 'px'
    mountain2.style.marginBottom = -value * 1.5 + 'px'
    main_logo.style.marginBottom = -value * 1.7 + 'px'

})
