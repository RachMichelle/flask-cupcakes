const BASEURL = "http://localhost:5000/api"

async function getCupcakeList(){
    let res = await axios.get(`${BASEURL}/cupcakes`);
    return res
}

async function addCupcakeList(){
    const res = await getCupcakeList();
    const cupcakes = res.data.cupcakes;

    for(cupcake of cupcakes){
        let addedCupcake= $(createHTML(cupcake));
        $('#cupcake-list').append(addedCupcake)
    }
}

function createHTML(cupcake){
    return `<li class="cupcake" data-id=${cupcake.id}>
    <img src="${cupcake.image}" style="max-height:200px;">
    Flavor: ${cupcake.flavor} | Size: ${cupcake.size} | Rating: ${cupcake.rating}
    <button class="delete-cupcake">X</button>
    </li>`
}

$('#cupcake-list').on('click', '.delete-cupcake', deleteCupcake)

async function deleteCupcake(evt){
    evt.preventDefault();
    const id=$(this).closest('li').data('id')
    await axios.delete(`${BASEURL}/cupcakes/${id}`)
    
    $(this).closest('li').remove()
}

$('#cupcake-form').on('submit', addCupcake)

async function addCupcake(evt){
    evt.preventDefault()

    flavor=$('#flavor-input').val()
    size=$('#size-input').val()
    rating=$('#rating-input').val()
    image=$('#image-input').val()

    const cupcake= await axios.post(`${BASEURL}/cupcakes`, {flavor, size, rating, image})

    let newCupcake = createHTML(cupcake.data.cupcake)

    $('#cupcake-list').append(newCupcake)

    $('#flavor-input').val('')
    $('#size-input').val('')
    $('#rating-input').val('')
    $('#image-input').val('')
}

addCupcakeList();