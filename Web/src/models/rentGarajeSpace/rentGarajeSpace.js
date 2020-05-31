// Firebase
import {auth, db} from '@/firebase'

/**
 * Represents the generic class for users.
 */
export default class RentGarajeSpace{
    constructor(){

    }


    /**
     * Returns all the rents in db.
     */
    async getAllRent() {          
        let rents = []

        let rentsDoc = await db.collection('rentGarajeSpace').get()
        rentsDoc.forEach( r => {      
            const rent = {}
            rent.pid = r.id
            rent.dates = r.data().dates
            rent.endHour = r.data().endHour
            rent.startHour = r.data().startHour
            rent.uidOwner = r.data().uidOwner
            rent.coordenateLNG = r.data().coordenateLNG
            rent.coordenateLAT = r.data().coordenateLAT

            rents.push(rent)
        })

        return rents        
    }

    /**
     * Get all rents of a parking.
     * @param {String} pid 
     */
    async getRentByPID(pid){
        
    }


    /**
     * Get all user rents within that parking.
     * @param {String} pid 
     * @param {String} uidRent 
     */
    async getMyRentByPID(pid, uidRent){
        let rents = []
        let rentsDoc = await db.collection('rentGarajeSpace').doc(pid).collection('usersRents').get()
        rentsDoc.forEach( r => {      
            const rent = {}

            rent.uidRent = r.data().uidRent
            if (rent.uidRent == uidRent){
                rent.approvedByOwner = r.data().approvedByOwner
                rent.coordenateLAT = r.data().coordenateLAT
                rent.coordenateLNG = r.data().coordenateLNG
                rent.dates = r.data().dates
                rent.endHour = r.data().endHour
                rent.startHour = r.data().startHour
                rents.push(rent)
            }
        })

        return rents    
    }

    /**
     * When user pay to rent a parking.
     * @param {String} pid of parking
     */
    async addRentToparking(pid, uidOwner, uidRent, dates, startHour, endHour, coordenateLAT, coordenateLNG) {
        let batch = db.batch()
        batch.set(db.collection('rentGarajeSpace').doc(pid).collection('usersRents').doc(uidRent), { 'approvedByOwner': false, 'uidRent': uidRent, 'dates': dates, 'startHour': startHour, 'endHour': endHour, 'coordenateLAT': coordenateLAT, 'coordenateLNG': coordenateLNG })
        batch.set(db.collection('users').doc(uidRent).collection('parkingsRent').doc(pid), { 'pid': pid, 'uidOwner': uidOwner})

        await batch.commit()
    }   
    
    
    async getRentsOfParking(pid){
        let rents = []
        let rentsDoc = await db.collection('rentGarajeSpace').doc(pid).collection('usersRents').get()
        rentsDoc.forEach( r => {      
            const rent = {}
            rent.uidRent = r.data().uidRent
            rent.approvedByOwner = r.data().approvedByOwner
            rent.coordenateLAT = r.data().coordenateLAT
            rent.coordenateLNG = r.data().coordenateLNG
            rent.dates = r.data().dates
            rent.endHour = r.data().endHour
            rent.startHour = r.data().startHour
            rents.push(rent)
            
        })

        return rents            
    }

    async acceptRent(rent, pid){
        let batch = db.batch()
        batch.update(db.collection('rentGarajeSpace').doc(pid).collection('usersRents').doc(rent.uidRent), { 'approvedByOwner': true})
        await batch.commit()
    }

    async denyRent(rent, pid){
        let batch = db.batch()
        batch.delete(db.collection('rentGarajeSpace').doc(pid).collection('usersRents').doc(rent.uidRent))
        batch.delete(db.collection('users').doc(rent.uidRent).collection('parkingsRent').doc(pid))

        await batch.commit()
    }
}