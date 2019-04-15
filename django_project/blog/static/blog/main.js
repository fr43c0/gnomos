function resize(){
    let h=window.outerHeight
    let w=window.outerWidth
    p='100%'
    if(320<w<640){
        console.log(w)
        let f=document.querySelectorAll('iframe');
        f.forEach(function(a){
            a=a.style.width=p;
        })
    
    }
    else{
        console.log('normal')
    }
}
