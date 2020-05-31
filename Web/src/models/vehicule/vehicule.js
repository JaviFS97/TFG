// Firebase
import {db} from '@/firebase'

/**
 * Represents the generic class for vehicules.
 */
export default class Vehicule{
    /**
     * Constructor for generic vehicules.
     * @param {String} plate 
     * @param {String} name 
     * @param {String} type 
     * @param {String} brand 
     * @param {String} model 
     * @param {String} height 
     * @param {String} width 
     * @param {String} depth 
     */
    constructor(plate, name, type, brand, model, height, width, depth){
        this.plate = plate;
        this.name = name;
        this.type = type;
        this.brand = brand;
        this.model = model;
        this.height = height;
        this.width = width;
        this.depth = depth;
    }

    /**
     * Add a vehicule to user(uid) list of vehicules in firebase database.
     * @param {String} uid: from user
     * @returns {Boolean} 
     */
    async createVehicule(uid){
        await this.existsVehicule(uid)
            .then( (res) => {
                let batch = db.batch()
                batch.set(db.collection('users').doc(uid).collection('vehicules').doc(this.plate), { 'name': this.name,
                                                                                                     'plate': this.plate,
                                                                                                     'type': this.type,
                                                                                                     'brand': this.brand,
                                                                                                     'model': this.model,
                                                                                                     'height': this.height,
                                                                                                     'width': this.width,
                                                                                                     'depth': this.depth
                                                                                                    })
                batch.set(db.collection('vehicules').doc(this.plate), { uid: uid })
                return batch.commit()
            })
            .catch( (error) => {
                new Promise ( resolve, reject => {
                    reject(error)
                })
            })
    }

    /**
     * Search a vehicule by plate in firebsae database.
     * @returns {Boolean}
     */
    async existsVehicule(uid) {
        let vehiculeDoc = await db.collection('vehicules').doc(this.plate).get()
        return new Promise( (resolve, reject) => {
            if(!vehiculeDoc.exists){
                resolve('vehicules not exists!')
            }
            else{
                if(vehiculeDoc.data().uid == uid)
                    resolve('this vehicule it\'s yours!')
                reject('vehicules exists!')
            }
        })
    }

    /**
     * 
     * @param {String} uid 
     */
    async deleteVehicule(uid){
        console.log(db.collection('vehicules').doc(this.plate))
        let batch = db.batch()
        batch.delete(db.collection('users').doc(uid).collection('vehicules').doc(this.plate))
        batch.delete(db.collection('vehicules').doc(this.plate))
        return batch.commit()
    }

}