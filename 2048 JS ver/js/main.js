var grid = 
[
[0,2,0,0],
[0,2,0,0],
[0,0,0,0],
[0,0,0,0]
]

console.log(grid[0][0])

function nextNumber(){
    var unoccupiedPos = []

    for(let i=0;i<4;i++){
        for(let j=0;j<4;j++){
            if(grid[i][j] == 0){
                unoccupiedPos.push([i,j])
            }
        }
    }

    console.log(unoccupiedPos)
}

nextNumber()