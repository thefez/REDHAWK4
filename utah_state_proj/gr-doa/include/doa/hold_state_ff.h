/* -*- c++ -*- */
/* 
 * Copyright 2017 <+YOU OR YOUR COMPANY+>.
 * 
 * This is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 * 
 * This software is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this software; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */


#ifndef INCLUDED_DOA_HOLD_STATE_FF_H
#define INCLUDED_DOA_HOLD_STATE_FF_H

#include <doa/api.h>
#include <gnuradio/sync_block.h>

namespace gr {
  namespace doa {

    /*!
     * \brief <+description of block+>
     * \ingroup doa
     *
     */
    class DOA_API hold_state_ff : virtual public gr::sync_block
    {
     public:
      typedef boost::shared_ptr<hold_state_ff> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of doa::hold_state_ff.
       *
       * To avoid accidental use of raw pointers, doa::hold_state_ff's
       * constructor is in a private implementation
       * class. doa::hold_state_ff::make is the public interface for
       * creating new instances.
       */
      static sptr make(int state, float scale0, float scale1);
      virtual void set_state(int new_state) = 0;
    };

  } // namespace doa
} // namespace gr

#endif /* INCLUDED_DOA_HOLD_STATE_FF_H */

